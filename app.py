import streamlit as st
from whisper_api import transcribe_audio
from gpt_utils import analyze_transcript

import tempfile

st.set_page_config(page_title="CallSage - AI Call Analyzer", layout="centered")
st.title("📞 CallSage: AI-Powered Call Analysis")

uploaded_file = st.file_uploader("Upload your call recording (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Transcribing with Whisper...")
    transcript = transcribe_audio(tmp_path)
    st.text_area("📄 Transcript", transcript, height=200)

    st.info("Analyzing with LLM...")
    summary, sentiment, action_points, model_used = analyze_transcript(transcript)

    st.subheader(f"📌 Summary (via {model_used})")
    st.write(summary)

    st.subheader("😊 Sentiment")
    st.write(sentiment)

    st.subheader("✅ Action Points")
    st.write(action_points)
