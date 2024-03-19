import os
import requests
import json

# Import any necessary libraries for audio processing
import librosa


def prepare_audio(file_path):
    # Load the audio file using librosa or another library
    audio, sr = librosa.load(file_path, sr=None)
    # Preprocess the audio as required for your model
    # This might include resampling, extracting features, etc.
    # For example, let's just resample the audio to 16kHz (adjust as needed)
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    # Convert the audio data to the format expected by your TensorFlow model
    # This is highly model-specific and needs to be adjusted
    # Here, we'll just use the raw audio for demonstration purposes
    return audio_resampled.tolist()


def send_request(audio_data):
    # Define the URL of your TensorFlow Serving API
    url = "http://localhost:8501/v1/models/objmodel:predict"
    # Construct the payload for the POST request
    data = json.dumps(
        {"signature_name": "__saved_model_init_op", "instances": [audio_data]}
    )
    # Make the request
    response = requests.post(url, data=data)
    return response.json()


def process_response(response):
    # Process the response from TensorFlow Serving
    # This is highly model-specific and needs to be adjusted
    # Here, we'll just print the response
    print(response)


def main(directory_path):
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(
            ".mp3"
        ):  # Adjust this condition based on your audio file format
            file_path = os.path.join(directory_path, filename)
            audio_data = prepare_audio(file_path)
            response = send_request(audio_data)
            process_response(response)


if __name__ == "__main__":
    directory_path = "output/"
    main(directory_path)
