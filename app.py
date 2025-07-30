import streamlit as st
from whisper_api import transcribe_audio
from gpt_utils import analyze_transcript
from db_utils import init_db, save_call, get_all_calls, get_call_by_id, clear_all_calls
import tempfile

# Set up page
st.set_page_config(page_title="CallSage - AI Call Analyzer", layout="centered")
st.markdown("## 📞 CallSage: AI-Powered Call Analysis")
st.write("Upload a voice call recording to get a transcript, summary, sentiment, and key action points.")

# Initialize database
init_db()

# Upload audio file
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

            st.markdown("###  Action Points")
            st.markdown("\n".join([f"- {line}" for line in action_points.split("\n") if line.strip()]))

            #  Save this call to history
            save_call(transcript, summary, sentiment, action_points, model_used)

        except Exception as e:
            st.error(" Something went wrong while analyzing the transcript.")
            st.exception(e)

#  Call History Section in Sidebar
st.sidebar.title("📂 Call History")

#  Add Clear History button
if st.sidebar.button("🗑 Clear Call History"):
    clear_all_calls()
    st.sidebar.success("History cleared!")
    st.experimental_rerun()

# Show previous calls
calls = get_all_calls()
selected = st.sidebar.selectbox("View Previous Call:", calls, format_func=lambda x: f"{x[1][:19]} - {x[2][:40]}" if x else "None")

if selected:
    call_id = selected[0]
    call_data = get_call_by_id(call_id)
    st.subheader("🕘 Timestamp")
    st.write(call_data[1])
    st.subheader("📄 Transcript")
    st.text_area("Transcript", call_data[2], height=200)
    st.subheader("📌 Summary")
    st.write(call_data[3])
    st.subheader("😊 Sentiment")
    st.write(call_data[4])
    st.subheader("✅ Action Points")
    st.write(call_data[5])
    st.caption(f"Model used: {call_data[6]}")

