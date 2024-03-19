import csv
import json
import os

import arrow
import librosa
import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
from scipy.signal import find_peaks
import numpy as np


def load_segments(directory):
    """Load all audio segments from a directory."""
    segments = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            path = os.path.join(directory, filename)
            audio = AudioSegment.from_file(path)
            segments.append((filename, audio))
    return segments


def classify_segments(segments, silence_threshold=-21):
    """Classify segments into 'sleep sound' or 'silence' based on dBFS threshold."""
    classified_segments = []
    for filename, segment in segments:
        if segment.dBFS < silence_threshold:
            classification = "silence"
        else:
            classification = "sleep sound"
        classified_segments.append((filename, classification))
    return classified_segments


def estimate_sleep_metrics(classified_segments, total_recording_time_seconds):
    """Estimate sleep metrics and calculate a simplified sleep efficiency score.

    Args:
        classified_segments: List of tuples with (filename, classification) of segments.
        total_recording_time_seconds: Total duration of the audio recording in seconds.

    Returns:
        A simplified sleep efficiency score out of 100.
    """
    total_time_of_seconds = 0
    for segment in classified_segments:
        total_time_of_seconds += segment["end"] - segment["start"]

    total_time_of_seconds = total_time_of_seconds / 1000

    # Calculate sleep efficiency
    SE = (total_time_of_seconds / total_recording_time_seconds) * 100

    return SE


def chop_audio_at_peaks(
    audio_path,
    output_folder,
):
    sound = AudioSegment.from_file(audio_path)
    dBFS = sound.dBFS
    chunks = detect_nonsilent(sound, min_silence_len=1000, silence_thresh=dBFS - 16)

    offset = 800
    segments = []
    for i, chunk in enumerate(chunks):
        begin_cut = chunk[0] - offset if chunk[0] - offset > 0 else 0
        end_cut = chunk[1] + offset if chunk[1] + offset < len(sound) else len(sound)
        newSound = sound[begin_cut:end_cut]
        newSound.export(f"{output_folder}/segment_{i}.mp3", format="mp3")
        segments.append(
            {
                "file_path": f"{output_folder}/segment_{i}.mp3",
                "start": begin_cut,
                "end": end_cut,
            }
        )

    return segments


def get_length_of_audio_file(file_path):
    """Get the length of an audio file in seconds."""
    length_of_file = librosa.get_duration(filename=file_path, sr=44100)
    return length_of_file


def analyze_audio(file_path, output_folder, audio_samples):
    """Analyze an audio file and return sleep metrics."""
    classified_segments = audio_samples
    total_recording_time_seconds = get_length_of_audio_file(
        file_path
    )  # Example: 8 hours * 60 minutes

    SE_score = int(
        estimate_sleep_metrics(classified_segments, total_recording_time_seconds)
    )

    return {
        "sleep_efficiency": SE_score,
        "segments": classified_segments,
    }


def create_graph_data(start_time, audio_samples, original_audio_file_path):
    starting_time = arrow.get(start_time)
    graph_data = []

    # Get the audio file length
    length_of_file = get_length_of_audio_file(original_audio_file_path)

    for second in range(0, int(length_of_file), 1):
        for audio_sample in audio_samples:
            if (
                int(audio_sample["start"] / 1000)
                <= second
                <= int(audio_sample["end"] / 1000)
            ):
                graph_data.append(
                    {"time": starting_time.shift(seconds=second).datetime, "value": 50}
                )
            else:
                graph_data.append(
                    {"time": starting_time.shift(seconds=second).datetime, "value": 100}
                )

    return graph_data


def get_class_names(class_map_csv_text):
    """Get class names from a CSV file."""

    # Read the CSV file
    class_names = []
    input_file = csv.DictReader(open(class_map_csv_text))
    for row in input_file:
        class_names.append(row["display_name"])
    return class_names


def categorize_sound(audio_file):
    class_names = get_class_names("helpers/yamnet_class_map.csv")
    waveform, sample_rate = librosa.load(audio_file, sr=16000, mono=True)

    url = "http://localhost:8501/v1/models/archive:predict"

    headers = {
        "Content-Type": "application/json",
    }

    data = json.dumps(
        {
            "signature_name": "serving_default",
            "inputs": {
                "waveform": waveform.tolist(),
            },
        }
    )

    response = requests.post(url, data=data, headers=headers)

    response_json = response.json()

    scores = np.array(response_json["outputs"]["output_0"])

    scores_mean = np.mean(scores, axis=0)
    inferred_class_index = np.argmax(scores_mean)
    inferred_class = class_names[inferred_class_index]

    # Adjust this function to include:
    top_n = 5  # Number of top predictions to consider
    top_class_indices = np.argsort(scores_mean)[-top_n:][::-1]  # Indices of top classes
    top_classes = [class_names[i] for i in top_class_indices]  # Names of top classes
    top_scores = [scores_mean[i] for i in top_class_indices]  # Scores of top classes

    return {"top_classes": top_classes, "confidences": top_scores}
