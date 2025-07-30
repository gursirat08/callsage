
import requests
import streamlit as st

REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

def transcribe_audio(file_path):
    # Step 1: Upload the audio file to file.io (get public URL)
    with open(file_path, "rb") as f:
        upload_response = requests.post("https://file.io", files={"file": f})
    if not upload_response.ok:
        st.error("Failed to upload audio file for transcription.")
        return "Upload failed."

    upload_url = upload_response.json().get("link")
    if not upload_url:
        st.error("No file link returned from upload service.")
        return "Upload failed."

    # Step 2: Send the URL to Replicate Whisper
    replicate_url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": "fdb6ac0bfa78e0f82f6e1c1e7185c29aa300b1f31fd640cfc3dc6f78df8fc00b",  # Whisper model version
        "input": {"audio": upload_url}
    }

    response = requests.post(replicate_url, headers=headers, json=payload)
    if not response.ok:
        st.error("Whisper API failed to start transcription.")
        return "Transcription failed."

    prediction = response.json()
    prediction_id = prediction["id"]

    # Step 3: Poll for the result
    status_url = f"{replicate_url}/{prediction_id}"
    while True:
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        if status_data["status"] == "succeeded":
            return status_data["output"]
        elif status_data["status"] in ["failed", "canceled"]:
            st.error("Transcription failed or was canceled.")
            return "Transcription failed."
