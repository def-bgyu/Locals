# Locals 🗽
### Explore NYC the Local Way

Locals is a RAG-powered web app that lets you discover NYC restaurants, cafes, and hidden gems through the lens of creators you actually trust.

Instead of generic Yelp reviews or SEO-optimized listicles, Locals indexes the real spoken recommendations from your favorite NYC lifestyle vloggers — the coffee shop they work from every Thursday, the restaurant they keep going back to, the neighborhood spot they swear by.

Tell us what you're feeling — the vibe, the cuisine, the mood — and Locals surfaces recommendations pulled directly from creator videos, with the exact quote and timestamp so you can see it for yourself.

---

## How it works

```
YouTube videos (your chosen creators)
        ↓  yt-dlp downloads audio
Audio files
        ↓  faster-whisper transcribes with timestamps
Transcript chunks
        ↓  LLM tags each chunk: place · routine · recommendation
Tagged chunks
        ↓  embedded and stored in ChromaDB
Vector index
        ↓  user picks mood + cuisine
Retrieval + LLM
        ↓
Result cards with creator quote + timestamp
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Audio download | yt-dlp |
| Transcription | faster-whisper (Whisper base) |
| Extraction | Groq (llama-3.3-70b) |
| Vector database | ChromaDB |
| Backend API | FastAPI |
| Frontend | Next.js + Tailwind CSS |
| LLM | Groq / Anthropic Claude |

---

## Project Structure

```
locals/
├── backend/
│   ├── ingestion/
│   │   ├── download.py          # pull audio from YouTube
│   │   ├── transcribe.py        # speech to text with timestamps
│   │   ├── extract.py           # tag places, cuisines, vibes
│   │   └── embed_and_store.py   # store in ChromaDB
│   ├── retrieval/
│   │   └── query.py             # search + generate answers
│   ├── data/
│   │   ├── audio/
│   │   └── transcripts/
│   └── main.py                  # FastAPI app
└── frontend/
    ├── app/
    │   ├── page.tsx             # home / mood picker
    │   ├── results/page.tsx     # result cards
    │   └── api/query/route.ts   # calls FastAPI
    └── components/
        ├── MoodPicker.tsx
        ├── PlaceCard.tsx
        └── CreatorBadge.tsx
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- ffmpeg

### Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # add your API keys
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### Run the pipeline

```bash
# 1. Download audio from a YouTube video
python ingestion/download.py

# 2. Transcribe the audio
python ingestion/transcribe.py

# 3. Extract places and recommendations
python ingestion/extract.py

# 4. Embed and store in ChromaDB
python ingestion/embed_and_store.py

# 5. Start the API server
uvicorn main:app --reload
```

---

## Environment Variables

```
ANTHROPIC_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=
```

---

*Built as a portfolio project exploring multimodal RAG pipelines and creator-driven discovery.*
