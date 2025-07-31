# streamlit_ui.py
import streamlit as st
import requests
import base64
import io

st.set_page_config(
    page_title="Prompta - Text to Media Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🎙️🖼️🎞️ Prompta - Text to Media Generator")

# 🛠️ Get Token FIRST
TOKEN = st.sidebar.text_input("🔑 API Token", type="password")
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# ✅ Display AFTER token is typed
if TOKEN:
    st.sidebar.write("Using token:", TOKEN)
else:
    st.sidebar.warning("⚠️ Please enter a valid API token to use the app.")

API_BASE = "http://localhost:8000"

# ==================================================
# Unified media rendering
# ==================================================
def render_media(response, label):
    content_type = response.headers.get("Content-Type", "")
    file_bytes = response.content

    if "audio" in content_type:
        st.audio(file_bytes, format=content_type)
    elif "video" in content_type:
        st.video(file_bytes)
    elif "image" in content_type:
        st.image(file_bytes, caption=label, use_container_width=True)
    else:
        try:
            # JSON fallback (video download_url case)
            data = response.json()
            if "download_url" in data:
                video_url = f"{API_BASE}{data['download_url']}"
                st.info("📥 Downloading video from URL...")
                video_resp = requests.get(video_url, headers=HEADERS)
                if video_resp.status_code == 200:
                    st.video(video_resp.content)
                else:
                    st.error(f"❌ Failed to download video from {video_url}")
            else:
                st.warning("⚠️ Unsupported media format or empty response.")
        except Exception:
            st.warning("⚠️ Unsupported media format or empty response.")

# ==================================================
# Sidebar Inputs
# ==================================================
st.sidebar.header("🛠️ Settings")

tab = st.sidebar.radio("Select Task", ["Text to Audio", "Text to Image", "Text to Video"])

# ==================================================
# Text to Audio
# ==================================================
if tab == "Text to Audio":
    st.subheader("🎤 Text to Audio")
    text = st.text_area("Enter text")
    voice = st.selectbox("Choose voice/language", ["en-US", "hi-IN", "te-IN", "ta-IN"])

    if st.button("🔊 Generate Audio"):
        with st.spinner("Generating audio..."):
            r = requests.post(
                f"{API_BASE}/api/v1/audio/generate",
                json={"text": text, "voice": voice},
                headers=HEADERS
            )
            if r.status_code == 200:
                render_media(r, "Generated Audio")
            else:
                st.error(f"❌ Failed: {r.json().get('detail', r.text)}")

# ==================================================
# Text to Image
# ==================================================
elif tab == "Text to Image":
    st.subheader("🖼️ Text to Image")
    prompt = st.text_area("Enter image prompt")
    style = st.selectbox("Choose style", ["nature", "technology", "urban", "abstract"])

    if st.button("🧠 Generate Image"):
        with st.spinner("Generating image from Unsplash..."):
            r = requests.post(
                f"{API_BASE}/api/v1/image/generate",
                json={"prompt": prompt, "style": style},
                headers=HEADERS
            )
            if r.status_code == 200:
                render_media(r, "Generated Image")
            else:
                try:
                    err = r.json().get('detail', 'Unknown error')
                except Exception:
                    err = r.text
                st.error(f"❌ Failed to fetch/display image: {err}")

# ==================================================
# Text to Video
# ==================================================
elif tab == "Text to Video":
    st.subheader("🎞️ Text to Video")
    prompt = st.text_area("Enter video prompt")
    tone = st.selectbox("Tone", ["formal", "casual", "emotional", "documentary"])
    domain = st.selectbox("Domain", ["health", "education", "governance", "entertainment"])
    environment = st.selectbox("Environment", ["urban", "rural", "nature", "futuristic"])

    if st.button("🎬 Generate Video"):
        with st.spinner("Generating video..."):
            r = requests.post(
                f"{API_BASE}/api/v1/video/generate",
                json={"prompt": prompt, "tone": tone, "domain": domain, "environment": environment},
                headers=HEADERS
            )
            if r.status_code == 200:
                render_media(r, "Generated Video")
            else:
                st.error(f"❌ Failed: {r.json().get('detail', r.text)}")


st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ for AI GovTech Challenge 2025")
