import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🎥 YouTube RAG Assistant", layout="centered")
API_URL = "http://localhost:8000/query"   # 🔁 Replace with your actual backend endpoint
PROCESS_URL = "http://localhost:8000/process"  # 🔁 Optional endpoint to process video if you have one

# ---------------- STATE MANAGEMENT ----------------
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- UI ----------------
st.title("🎥 YouTube RAG Assistant")
st.markdown("Upload a YouTube video ID, then ask any questions about its content!")

# ----------- STEP 1: UPLOAD VIDEO -----------
if not st.session_state.video_loaded:
    video_id = st.text_input("🔗 Enter YouTube Video ID:", placeholder="e.g. dQw4w9WgXcQ")
    if st.button("🎬 Load Video"):
        if not video_id:
            st.warning("Please enter a valid YouTube Video ID.")
        else:
            with st.spinner("Processing video transcript..."):
                try:
                    # Send request to your backend
                    payload = {"video_id": video_id}
                    response = requests.post(PROCESS_URL, json=payload, timeout=90)

                    if response.status_code == 200:
                        st.session_state.video_loaded = True
                        st.session_state.video_id = video_id
                        st.success("✅ Video processed successfully! You can now ask questions.")
                    else:
                        st.error(f"Server error: {response.status_code}\n{response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

else:
    # ----------- STEP 2: ASK QUESTIONS -----------
    st.info(f"🎬 Video loaded: `{st.session_state.video_id}`")

    # Optional YouTube video preview
    st.video(f"https://www.youtube.com/watch?v={st.session_state.video_id}")

    st.markdown("### 💬 Ask questions about the video")
    question = st.text_input("Your question:", placeholder="What is this video about?")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Fetching answer..."):
                try:
                    payload = {
                        "video_id": st.session_state.video_id,
                        "question": question
                    }
                    response = requests.post(API_URL, json=payload, timeout=60)

                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("answer", "No answer returned.")
                        st.session_state.chat_history.append((question, answer))
                        st.success("✅ Answer received!")
                    else:
                        st.error(f"Server error: {response.status_code}\n{response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

    # ----------- DISPLAY CHAT HISTORY -----------
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("🧠 Chat History")
        for i, (q, a) in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")

    if st.button("🔄 Upload New Video"):
        st.session_state.video_loaded = False
        st.session_state.chat_history = []
        st.session_state.video_id = None
        st.experimental_rerun()
