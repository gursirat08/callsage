# whisper_api.py
import requests
import streamlit as st
import time

ASSEMBLYAI_API_KEY = st.secrets["ASSEMBLYAI_API_KEY"]

def transcribe_audio(file_path):
    # Step 1: Upload audio file
    with open(file_path, "rb") as f:
        upload_response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers={"authorization": ASSEMBLYAI_API_KEY},
            files={"file": f}
        )
    if not upload_response.ok:
        st.error("File upload to AssemblyAI failed.")
        return "Upload failed."

    audio_url = upload_response.json()["upload_url"]

    # Step 2: Start transcription
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json={"audio_url": audio_url},
        headers={"authorization": ASSEMBLYAI_API_KEY}
    )
    if not transcript_response.ok:
        st.error("Transcription request failed.")
        return "Transcription failed."

    transcript_id = transcript_response.json()["id"]

    # Step 3: Poll until transcription is done
    while True:
        poll_response = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers={"authorization": ASSEMBLYAI_API_KEY}
        )
        status = poll_response.json()["status"]
        if status == "completed":
            return poll_response.json()["text"]
        elif status == "error":
            st.error("Transcription failed.")
            return "Transcription failed."
        time.sleep(2)
