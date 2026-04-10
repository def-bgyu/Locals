locals/
├── .gitignore
├── README.md
│
├── backend/                         ← Python / FastAPI
│   ├── main.py                      ← FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example                 ← copy to .env and add your keys
│   │
│   ├── ingestion/                   ← Phase 1: building the pipeline
│   │   ├── __init__.py
│   │   ├── download.py              ← pull audio from YouTube via yt-dlp
│   │   ├── transcribe.py            ← speech to text via faster-whisper
│   │   ├── extract.py               ← tag places, cuisines, vibes, sentiment
│   │   └── embed_and_store.py       ← chunk + embed + store in ChromaDB
│   │
│   ├── retrieval/                   ← Phase 2: querying the pipeline
│   │   ├── __init__.py
│   │   └── query.py                 ← search + ask Claude + return results
│   │
│   └── data/                        ← local data (git ignored)
│       ├── audio/                   ← downloaded audio files (.mp3/.wav)
│       └── transcripts/             ← raw transcript JSON files
│
└── frontend/                        ← Next.js
    ├── next.config.ts
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── package.json
    │
    ├── public/                      ← static assets
    │
    └── app/                         ← Next.js App Router
        ├── layout.tsx               ← root layout (fonts, metadata)
        ├── globals.css              ← global styles + Tailwind
        ├── page.tsx                 ← home screen / mood picker
        │
        ├── results/
        │   └── page.tsx             ← results cards page
        │
        └── api/
            └── query/
                └── route.ts         ← API route that calls FastAPI backend