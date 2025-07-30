# streamlit_ui.py
import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="Prompta - Text to Media Generator",
    page_icon="🎙️",  # You can replace with uploaded image: 'logo/favicon.ico'
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🎙️🖼️🎞️ Prompta - Text to Media Generator")

API_BASE = "http://localhost:8000"  # change if deployed

# Helper to play audio/video in Streamlit
def render_media(file_bytes, media_type, label):
    b64 = base64.b64encode(file_bytes).decode()
    if media_type == "audio":
        st.audio(f"data:audio/wav;base64,{b64}", format="audio/wav")
    elif media_type == "video":
        st.video(f"data:video/mp4;base64,{b64}")
    elif media_type == "image":
        st.image(file_bytes, caption=label, use_column_width=True)

# Sidebar inputs
st.sidebar.header("🛠️ Settings")
TOKEN = st.sidebar.text_input("🔑 API Token", type="password")
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# Tabs
tab = st.sidebar.radio("Select Task", ["Text to Audio", "Text to Image", "Text to Video"])

if tab == "Text to Audio":
    st.subheader("🎤 Text to Audio")
    text = st.text_area("Enter text")
    voice = st.selectbox("Choose voice/language", ["en-US", "hi-IN", "te-IN", "ta-IN"])
    
    if st.button("🔊 Generate Audio"):
        with st.spinner("Generating audio..."):
            r = requests.post(f"{API_BASE}/audio/generate", json={"text": text, "voice": voice}, headers=HEADERS)
            if r.status_code == 200:
                render_media(r.content, "audio", "Generated Audio")
            else:
                st.error(f"❌ Failed: {r.json().get('detail')}")

elif tab == "Text to Image":
    st.subheader("🖼️ Text to Image")
    prompt = st.text_area("Enter image prompt")
    model = st.selectbox("Choose model", ["sdxl", "deepfloyd", "kandinsky"])

    if st.button("🧠 Generate Image"):
        with st.spinner("Generating image..."):
            r = requests.post(f"{API_BASE}/image/generate", json={"prompt": prompt, "model": model}, headers=HEADERS)
            if r.status_code == 200:
                render_media(r.content, "image", "Generated Image")
            else:
                st.error(f"❌ Failed: {r.json().get('detail')}")

elif tab == "Text to Video":
    st.subheader("🎞️ Text to Video")
    prompt = st.text_area("Enter video prompt")
    tone = st.selectbox("Tone", ["formal", "casual", "emotional", "documentary"])
    domain = st.selectbox("Domain", ["health", "education", "governance", "entertainment"])
    environment = st.selectbox("Environment", ["urban", "rural", "nature", "futuristic"])

    if st.button("🎬 Generate Video"):
        with st.spinner("Generating video..."):
            r = requests.post(
                f"{API_BASE}/video/generate",
                json={"prompt": prompt, "tone": tone, "domain": domain, "environment": environment},
                headers=HEADERS
            )
            if r.status_code == 200:
                render_media(r.content, "video", "Generated Video")
            else:
                st.error(f"❌ Failed: {r.json().get('detail')}")

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ for AI GovTech Challenge 2025")
