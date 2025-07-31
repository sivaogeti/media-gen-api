# streamlit_ui.py

import streamlit as st
import requests
import base64
from PIL import Image
import io
import os
import tempfile

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
    st.sidebar.write("Sending headers:", HEADERS)
else:
    st.sidebar.warning("⚠️ Please enter a valid API token to use the app.")

API_BASE = "http://localhost:8000"

#API_BASE = "https://2255d6a4793d.ngrok-free.app"

def render_media(file_bytes, media_type, caption):
    b64 = base64.b64encode(file_bytes).decode()
    if media_type == "audio":
        st.audio(f"data:audio/wav;base64,{b64}", format="audio/wav")
    elif media_type == "video":
        st.video(f"data:video/mp4;base64,{b64}")
    elif media_type == "image":
        try:
            # Validate if it's a valid image
            img = Image.open(io.BytesIO(file_bytes))
            st.image(img, caption=caption)
        except Exception as e:
            st.warning("⚠️ Cannot render image. It may be corrupt or empty.")
            st.code(str(e))

# Sidebar inputs
st.sidebar.header("🛠️ Settings")
#TOKEN = st.sidebar.text_input("🔑 API Token", type="password")
#HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

voice = st.selectbox("Choose voice", ["en", "hi", "te", "ta"])
voice_map = {
    "en": "en-US",
    "hi": "hi-IN",
    "te": "te-IN",
    "ta": "ta-IN"
}

tab = st.sidebar.radio("Select Task", ["Text to Audio", "Text to Image", "Text to Video"])

if tab == "Text to Audio":
    st.subheader("🎤 Text to Audio")
    text = st.text_area("Enter text")
    voice = st.selectbox("Choose language", ["English", "Hindi", "Telugu", "Tamil"])
    voice_map = {
        "English": ("en-US", "en"),
        "Hindi": ("hi-IN", "hi"),
        "Telugu": ("te-IN", "te"),
        "Tamil": ("ta-IN", "ta")
    }
    voice_code, lang_code = voice_map[voice]

    if st.button("🔊 Generate Audio"):
        with st.spinner("Generating audio..."):
            r = requests.post(
                f"{API_BASE}/api/v1/audio/generate", 
                json={
                    "text": text,
                    "voice": voice_code,
                    "language": lang_code
                },
                headers=HEADERS
            )
            if r.status_code == 200:
                try:
                    data = r.json()
                    st.code(data, language="json")  # Debug: show full JSON response in UI

                    if "download_url" in data:
                        download_url = f"{API_BASE}{data['download_url']}"
                        audio_resp = requests.get(download_url, headers=HEADERS)
                        if audio_resp.status_code == 200:
                            render_media(audio_resp.content, "audio", "Generated Audio")
                        else:
                            st.error("❌ Failed to download audio file.")
                    else:
                        st.error("❌ `download_url` not found in API response.")
                        st.code(data)
                except Exception as e:
                    st.error("❌ Failed to parse API response.")
                    st.code(r.text)
                    st.exception(e)
            else:
                st.error(f"❌ Failed: {r.json().get('detail')}")


elif tab == "Text to Image":
    st.subheader("🖼️ Text to Image")
    prompt = st.text_area("Enter image prompt")
    style = st.selectbox("Choose Style", ["sdxl", "deepfloyd", "kandinsky"])

    if st.button("🧠 Generate Image"):
        with st.spinner("Generating image..."):
            r = requests.post(
                f"{API_BASE}/api/v1/image/generate", 
                json={"prompt": prompt, "style": style},  # ✅ correct key
                headers=HEADERS
            )
            if r.status_code == 200:
                try:
                    res_json = r.json()
                    download_url = res_json.get("download_url")
                    if not download_url:
                        st.error("No download URL returned.")
                    else:
                        download_full_url = f"{API_BASE}{download_url}"
                        image_response = requests.get(download_full_url, headers={"accept": "image/png"}, allow_redirects=True)
                        if image_response.status_code != 200:
                            st.error("❌ Failed to download image.")
                            st.code(image_response.text)
                            st.write("Status:", image_response.status_code)
                            st.write("Headers:", image_response.headers)
                        st.write(image_response.status_code, image_response.headers)
                        render_media(image_response.content, "image", "Generated Image")
                except Exception as e:
                    st.error(f"⚠️ Failed to fetch/display image: {str(e)}")
                    st.code(r.text)
            else:
                try:
                    detail = r.json().get("detail")
                except Exception:
                    detail = r.text  # fallback to raw response text (may be empty or HTML)

                st.error(f"❌ Failed: {detail}")                

elif tab == "Text to Video":
    st.subheader("🎞️ Text to Video")
    prompt = st.text_area("Enter video prompt")
    tone = st.selectbox("Tone", ["formal", "casual", "emotional", "documentary"])
    domain = st.selectbox("Domain", ["health", "education", "governance", "entertainment"])
    environment = st.selectbox("Environment", ["urban", "rural", "nature", "futuristic"])

    transcript = st.text_area("Transcript (optional - for subtitles)", height=100)
    enhance = st.checkbox("✨ Add Subtitles and Background Music")

    if st.button("🎬 Generate Video"):
        with st.spinner("Generating video..."):
            r = requests.post(
                f"{API_BASE}/api/v1/video/generate",
                json={"prompt": prompt, "tone": tone, "domain": domain, "environment": environment},
                headers=HEADERS
            )
            if r.status_code == 200:
                try:
                    data = r.json()
                    st.code(data, language="json")

                    download_url = data.get("download_url")
                    if not download_url:
                        st.error("⚠️ No download URL received.")
                    else:
                        full_video_url = f"{API_BASE}{download_url}"
                        video_response = requests.get(full_video_url, headers=HEADERS)
                        if video_response.status_code == 200:
                            video_bytes = video_response.content
                            st.write("📦 Video size (bytes):", len(video_bytes))

                            if enhance and transcript:
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
                                    tmp_vid.write(video_bytes)
                                    tmp_vid_path = tmp_vid.name

                                srt_path = generate_srt_from_text(transcript, output_path="streamlit_subs.srt")
                                enhanced_path = "streamlit_final_video.mp4"
                                enhance_video_with_subtitles_and_bgm(
                                    video_path=tmp_vid_path,
                                    srt_path=srt_path,
                                    bgm_path="default_bgm.mp3",
                                    output_path=enhanced_path
                                )

                                with open(enhanced_path, "rb") as f:
                                    render_media(f.read(), "video", "Enhanced Video")
                            else:
                                st.video(video_bytes)
                        else:
                            st.error("❌ Failed to download video.")
                except Exception as e:
                    st.error("❌ Error parsing response or rendering video.")
                    st.code(r.text)
                    st.exception(e)
            else:
                try:
                    st.error(f"❌ Failed: {r.json().get('detail')}")
                except:
                    st.error(f"❌ Failed: {r.text}")


st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ for AI GovTech Challenge 2025")
