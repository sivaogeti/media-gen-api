# 🎙️ Media Generation API

A FastAPI-based backend to generate audio, images, video, and PPT from user inputs. 
Supports BLEU/CLIP metrics, token-based authentication, and stores metadata in SQLite/Postgres.

A modular, RESTful FastAPI solution that converts text input into:
- 🎥 Video
- 🖼️ Image/Graphics
- 🔊 Audio


---

## 🚀 Features

- Text → Video: Tone, domain, and environment-aware video generation.
- Text → Audio: Context-aware voice synthesis with emotional tone and language support.
- Text → Graphics: Visual generation using parameter-based prompts.
- BLEU/CLIP metrics for prompt-output fidelity.
- Token-based authentication for secure API use.
- Dockerized for easy deployment
- Optional Streamlit/React UI
- Swagger UI: `http://localhost:8000/docs`

---

### 📁 Project Structure
media-gen-api/
├── app/
│   ├── api/v1/               # Versioned API endpoints
│   ├── auth/                 # Token-based auth
│   ├── services/             # Core media generation logic
│   └── main.py               # FastAPI entry point
├── tests/                    # Unit/integration tests
├── requirements.txt
└── README.md

---

## 📦 Installation
🚀 Run Locally
1. Clone repo & create virtual environment

git clone https://github.com/yourorg/media-gen-api.git
cd media-gen-api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt

3. Run the API

uvicorn app.main:app --reload

Access docs: http://127.0.0.1:8000/docs

---
### 🔐 Authentication
Use Bearer <your_token> in the Authorize button or headers.

---
### 📡 API Endpoints Summary
| Endpoint                  | Method | Description               |
|--------------------------|--------|---------------------------|
| /api/v1/audio/generate   | POST   | Generate audio from text |
| /api/v1/image/generate   | POST   | Generate image from text |
| /api/v1/video/generate   | POST   | Generate video from text |
| /api/v1/download         | GET    | Download generated file  |

---
###📦 Deployment (Streamlit/Optional UI)
Option 1: Run with Streamlit (for demo)
streamlit run streamlit_ui.py

Option 2: Docker (Production-ready)
docker build -t media-gen-api .
docker run -p 8000:8000 media-gen-api

---
### 📊 Metrics Logging (Optional)
- BLEU score and CLIPScore (WIP)
- Latency, GPU/CPU tracking
- Log file: logs/generation.log

---
#### 📋 Submission Checklist
- ✅ RESTful modular architecture
- ✅ Multi-format (MP4, PNG, WAV)
- ✅ Token Auth + Swagger UI
- ✅ Compatible with DD/PIB via API
- ✅ Streamlit demo app (optional)

