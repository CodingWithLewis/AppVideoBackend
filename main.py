import base64
import os
import uuid
from datetime import datetime
from typing import List

import firebase_admin
import openfoodfacts
import requests
import arrow
from fastapi import FastAPI, UploadFile, Form, File, HTTPException, BackgroundTasks
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel

from aiphoto import detect_faces
from helpers.ai_model import train_ai_images
from helpers.firebase_helpers import upload_to_storage
from helpers.sleep import (
    chop_audio_at_peaks,
    categorize_sound,
    analyze_audio,
    create_graph_data,
)
from yuka import format_product
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/image-to-image/masking"

if os.getenv("FIRE_MODE") == "aiimage":
    print("AI Image mode")
    cred = credentials.Certificate("aiphotos.json")
    f_app = firebase_admin.initialize_app(
        cred, {"storageBucket": "aiphotos-fc599.appspot.com"}
    )
elif os.getenv("FIRE_MODE") == "yuka":
    print("Yuka mode")
    cred = credentials.Certificate("yuka.json")
    f_app = firebase_admin.initialize_app(cred, {})

else:
    print("sleep tracking mode")
    cred = credentials.Certificate("sleep.json")
    f_app = firebase_admin.initialize_app(
        cred, {"storageBucket": "sleep-app-mrlfi4.appspot.com"}
    )

db = firestore.client()
api = openfoodfacts.API(user_agent="Lewka App")

app = FastAPI(debug=True)


class Item(BaseModel):
    barcode: str
    user_id: str


@app.post("/items/")
async def create_scan(item: Item):
    # Here you can add the code to handle the barcode, for example, call the OpenFoodFacts API

    # See if the user already scanned this
    query = (
        db.collection("scans")
        .where(filter=FieldFilter("scanned_by", "==", item.user_id))
        .where(filter=FieldFilter("barcode", "==", item.barcode))
    ).stream()

    query_list = list(query)  # Convert the generator to a list

    if len(query_list) > 0:
        scanned_id = query_list[0].id
        return {"error": "User already scanned this product", "id": scanned_id}

    # See if the product is already in the cache
    doc_ref = db.collection("products").document(item.barcode)

    if doc_ref.get().exists:
        print("Product found in cache")
        food_item = doc_ref.get().to_dict()
        return food_item
    else:
        food_item = api.product.get(
            item.barcode,
            fields=[
                "product_name",
                "nutriments",
                "nutriscore_grade",
                "image_url",
                "brand_owner",
                "additives_n",
                "nutriscore",
                "nutriscore_2023_tags",
            ],
        )

    if food_item is None:
        return {"error": "Product not found"}

    random_uuid = str(uuid.uuid4())

    food_item = format_product(food_item, item.user_id, item.barcode)
    # Save to scans collection in Firestore

    food_item["id"] = random_uuid

    db.collection("scans").document(random_uuid).set(food_item)

    if not doc_ref.get().exists:
        doc_ref.set(food_item)

    return food_item


@app.post("/analyze-image/")
async def analyze_image(image: UploadFile, user_id: str = Form(...)):

    contents = await image.read()  # Await the read() coroutine
    random_uuid = str(uuid.uuid4())
    filepath = f"images/{random_uuid}/"
    Path(filepath + "masks").mkdir(parents=True, exist_ok=True)
    with open(f"{filepath}{image.filename}", "wb") as f:
        f.write(contents)

    public_url = await upload_to_storage(f"{filepath}{image.filename}")

    masks = await detect_faces(
        contents, image.filename, filepath
    )  # Await the detect_faces() coroutine

    document = (
        db.collection("image_uploads")
        .document(random_uuid)
        .set(
            {
                "filename": image.filename,
                "user_id": user_id,
                "id": random_uuid,
                "public_url": public_url,
                "masks": masks,
            },
        )
    )

    return {
        "id": random_uuid,
    }


@app.post("/image-masking/")
async def alter_ai_image(
    text_prompts: List[str] = Form(...),
    init_image: UploadFile = File(...),
    mask_image: UploadFile = File(...),
    mask_source: str = Form("MASK_IMAGE_WHITE"),
    cfg_scale: float = Form(7),
    samples: int = Form(1),
    seed: int = Form(0),
    steps: int = Form(30),
    style_preset: str = Form(None),
    photo_uuid: str = Form(None),
):
    # Prepare multipart data
    data = {}
    files = {
        "init_image": (
            init_image.filename,
            await init_image.read(),
            init_image.content_type,
        ),
        "mask_image": (
            mask_image.filename,
            await mask_image.read(),
            mask_image.content_type,
        ),
    }

    for i, prompt in enumerate(text_prompts):
        data[f"text_prompts[{i}][text]"] = prompt
        data[f"text_prompts[{i}][weight]"] = (
            1  # Assuming a default weight of 1 for simplicity
        )

    data.update(
        {
            "mask_source": mask_source,
            "cfg_scale": cfg_scale,
            "samples": samples,
            "seed": seed,
            "steps": steps,
            "style_preset": style_preset,
        }
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('STABILITY_AI_APIKEY')}",
        "Accept": "application/json",
    }

    # Forward the request to Stability AI API
    response = requests.post(STABILITY_API_URL, headers=headers, files=files, data=data)

    if response.status_code != 200:
        print(response.text)
        raise HTTPException(
            status_code=response.status_code, detail="Error from Stability AI API"
        )

    response = response.json()

    image_data = base64.b64decode(response["artifacts"][0]["base64"])
    date = arrow.get(datetime.utcnow()).timestamp()
    file_path = f"images/{photo_uuid}/{date}.jpg"
    with open(file_path, "wb") as file:
        file.write(image_data)

    public_url = await upload_to_storage(file_path)

    query = (
        db.collection("image_uploads")
        .document(photo_uuid)
        .update(
            {"public_url": public_url},
        )
    )

    return {
        "public_url": public_url,
    }


@app.post("/create-ai-images/{user_id}/")
async def upload_ai_images(
    user_id: str, images: List[UploadFile], background_tasks: BackgroundTasks
):
    file_path = f"images/aiimages/{user_id}/training"
    Path(file_path).mkdir(parents=True, exist_ok=True)
    for index, image in enumerate(images):
        contents = await image.read()
        with open(f"{file_path}/{index}.jpg", "wb") as f:
            f.write(contents)
    background_tasks.add_task(train_ai_images, user_id)
    return {"message": "Images uploaded and training started"}


@app.post("/create-sleep-score/")
async def create_sleep_score(
    audio_file: UploadFile, user_id: str = Form(...), started_at: datetime = Form(...)
):
    random_uuid = str(uuid.uuid4())
    filepath = f"audio/{random_uuid}/"
    Path(filepath).mkdir(parents=True, exist_ok=True)
    filepath_output = f"audio/{random_uuid}/output"
    Path(filepath_output).mkdir(parents=True, exist_ok=True)

    with open(f"{filepath}{audio_file.filename}", "wb") as f:
        f.write(await audio_file.read())
    # Chop audio files at peaks
    audio_segments = chop_audio_at_peaks(
        f"{filepath}{audio_file.filename}", filepath_output
    )
    # Save all files to storage and save the public urls to Firestore
    public_urls = []
    for file in audio_segments:
        public_url = await upload_to_storage(file["file_path"])
        categories = categorize_sound(file["file_path"])

        category = categories["top_classes"][0]

        if category == "Breathing":
            category = categories["top_classes"][1]

        public_urls.append(
            {
                "public_url": public_url,
                "category": category,
                "start": file["start"],
                "end": file["end"],
                "file_path": file["file_path"],
            }
        )

    score = analyze_audio(
        f"{filepath}{audio_file.filename}", filepath_output, public_urls
    )

    # Save the public urls to Firestore

    db.collection("sleep_scores").document(random_uuid).set(
        {
            "user_id": user_id,
            "audio_files": public_urls,
            "sleep_score": score["sleep_efficiency"],
            "scanned_at": started_at,
            "uuid": random_uuid,
        }
    )

    ref = db.collection("sleep_scores").document(random_uuid)

    graph_data = create_graph_data(
        started_at, public_urls, f"{filepath}{audio_file.filename}"
    )
    for data in graph_data:
        db.collection("sleep_scores").document(random_uuid).collection(
            "graph_data"
        ).add(data)

    return {"message": "Audio files uploaded and sleep score created", "uuid": ref.path}


@app.post("/categorize-sleep-sounds/")
async def categorize_sleep_sounds(audio_file: UploadFile):
    file_path = f"audio/{audio_file.filename}"
    with open(file_path, "wb") as f:
        f.write(await audio_file.read())

    prediction = categorize_sound(file_path)
    return prediction
