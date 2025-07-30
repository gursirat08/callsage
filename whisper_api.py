import requests
import streamlit as st

REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
        data = {
            "version": "fdb6ac0bfa78e0f82f6e1c1e7185c29aa300b1f31fd640cfc3dc6f78df8fc00b",
            "input": {"audio": f}
        }
        response = requests.post("https://api.replicate.com/v1/predictions", json=data, headers=headers)
        response.raise_for_status()
        prediction = response.json()
        return prediction.get("output", "Transcription failed.")
