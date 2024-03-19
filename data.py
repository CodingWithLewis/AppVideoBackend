import asyncio
from pathlib import Path

import firebase_admin
from helpers.firebase_helpers import upload_to_storage
from firebase_admin import credentials, firestore


cred = credentials.Certificate("aiphotos.json")
f_app = firebase_admin.initialize_app(
    cred, {"storageBucket": "aiphotos-fc599.appspot.com"}
)
db = firestore.client()

images = Path("aimodels").glob("*.png")


async def fn():
    for image_path in images:
        public_url = await upload_to_storage(f"aimodels/{image_path.name}")
        db.collection("ai_images").add({"photo_url": public_url})


loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(fn())
loop.close()
