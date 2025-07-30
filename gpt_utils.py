import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_model(prompt, model="openrouter/gpt-4"):
    try:
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"], model
    except:
        fallback_model = "openrouter/claude-instant-v1"
        data["model"] = fallback_model
        response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"], fallback_model

def analyze_transcript(transcript):
    summary, model_used = call_model(
        f"Summarize the following conversation:\n\n{transcript}"
    )
    sentiment, _ = call_model(
        f"What is the sentiment of this conversation?\n\n{transcript}",
        model_used
    )
    action_points, _ = call_model(
        f"List the key action items from this conversation:\n\n{transcript}",
        model_used
    )
    return summary, sentiment, action_points, model_used.split("/")[-1]


