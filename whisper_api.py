# whisper_api.py
import requests
import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        files = {
            'file': audio_file,
            'model': (None, 'whisper-1')
        }
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files)

        # DEBUG: Print full response for debugging
        if not response.ok:
            st.error("OpenAI Whisper API call failed.")
            st.code(response.text)  # <-- shows the actual error details from OpenAI
            return "Transcription failed."

        return response.json().get("text", "Transcription failed.")
