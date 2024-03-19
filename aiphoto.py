from google.cloud import vision
from PIL import Image, ImageDraw

from helpers.firebase_helpers import upload_to_storage


async def detect_faces(image: bytes, image_name: str, filepath: str):
    """Detects faces in an image and creates masks for eyes, mouth, and nose."""
    # Initialize the Google Cloud Vision client
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image)

    # Perform face detection
    response = client.face_detection(image=image)
    faces = response.face_annotations
    mask_image_paths = []

    # Process each face found
    for face_index, face in enumerate(faces):
        features = {
            "left_eye": {"x": [], "y": []},
            "right_eye": {"x": [], "y": []},
            "mouth": {"x": [], "y": []},
            "nose": {"x": [], "y": []},
        }

        # Collect coordinates for eyes, mouth, and nose
        for landmark in face.landmarks:
            if "LEFT_EYE" in landmark.type.name:
                features["left_eye"]["x"].append(landmark.position.x)
                features["left_eye"]["y"].append(landmark.position.y)
            elif "RIGHT_EYE" in landmark.type.name:
                features["right_eye"]["x"].append(landmark.position.x)
                features["right_eye"]["y"].append(landmark.position.y)
            elif "MOUTH" in landmark.type.name:
                features["mouth"]["x"].append(landmark.position.x)
                features["mouth"]["y"].append(landmark.position.y)
            elif "NOSE" in landmark.type.name:
                features["nose"]["x"].append(landmark.position.x)
                features["nose"]["y"].append(landmark.position.y)

        # Calculate bounding boxes for each feature with a margin and create masks
        margin = 15  # Adjust the margin size as needed
        for feature_name, feature in features.items():
            if (
                feature["x"] and feature["y"]
            ):  # Check if there are coordinates to process
                box = [
                    min(feature["x"]) - margin,
                    min(feature["y"]) - margin,
                    max(feature["x"]) + margin,
                    max(feature["y"]) + margin,
                ]

                # Create a black image for the mask
                original_image = Image.open(f"{filepath}{image_name}")
                mask_image = Image.new("L", original_image.size, 0)
                draw = ImageDraw.Draw(mask_image)

                # Draw a white rectangle for the feature area
                draw.rectangle(box, fill=255)

                # Save the mask image
                mask_image_path = f"{filepath}masks/mask_{feature_name}.png"
                mask_image.save(mask_image_path)
                mask_image_paths.append(await upload_to_storage(mask_image_path))

    # Check for errors in the response
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return mask_image_paths
