
import streamlit as st
from whisper_api import transcribe_audio
from gpt_utils import analyze_transcript
import tempfile

st.set_page_config(page_title="CallSage - AI Call Analyzer", layout="centered")

st.markdown("## 📞 CallSage: AI-Powered Call Analysis")
st.write("Upload a voice call recording to get a transcript, summary, sentiment, and key action points.")

uploaded_file = st.file_uploader("🎧 Upload your audio file (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-4:]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("⏳ Transcribing audio with Whisper..."):
        transcript = transcribe_audio(tmp_path)

    st.subheader("📄 Transcript")
    st.text_area("Full Transcript", transcript, height=200)

    with st.spinner("🔍 Analyzing transcript with LLM..."):
        try:
            summary, sentiment, action_points, model_used = analyze_transcript(transcript)

            st.markdown(f"### 📌 Summary (Model: `{model_used}`)")
            st.success(summary)

            st.markdown("### 😊 Sentiment")
            st.info(sentiment)

            st.markdown("### ✅ Action Points")
            st.markdown("\n".join([f"- {line}" for line in action_points.split("\n") if line.strip()]))

        except Exception as e:
            st.error("❌ Something went wrong while analyzing the transcript.")
            st.exception(e)
