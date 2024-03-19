from firebase_admin import storage


async def upload_to_storage(file_path: str):
    # Get a reference to the storage service
    bucket = storage.bucket()

    # Create a new blob and upload the file's content.
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)
    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url
