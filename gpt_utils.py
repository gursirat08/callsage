import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_model(prompt, model="anthropic/claude-instant-v1"):
    try:
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                 headers={
                                     "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                                     "Content-Type": "application/json"
                                 }, 
                                 json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"], model
    except requests.exceptions.HTTPError as e:
        st.error(f"GPT model API call failed: {e}")
        raise



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


