import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.GenerativeModel("gemini-2.0-flash")

def extract_batch(chunks: list) -> list:
    """
    Takes a batch of chunks and extracts all of them in ONE API call.
    Much more efficient than one call per chunk.
    """

    numbered = ""
    for i, chunk in enumerate(chunks):
        numbered += f"[{i}] [{chunk['timestamp_label']}] {chunk['text']}\n"

    prompt = f"""
You are analyzing transcript chunks from a NYC lifestyle vlogger.

For each chunk, determine if it contains:
- A PLACE mention (restaurant, cafe, bar, park, shop)
- A ROUTINE mention (morning routine, workout, habit)  
- A RECOMMENDATION (something they explicitly suggest)

Respond with a JSON array only. No markdown. No explanation. Just raw JSON.
One object per chunk, in the same order.

For useful chunks:
{{"index": 0, "is_useful": true, "category": "place", "place_name": "name or null", "cuisine_type": "cuisine or null", "vibe": "cozy|trendy|casual|upscale|hidden-gem|classic", "summary": "one sentence", "sentiment": "positive|neutral|negative"}}

For filler chunks:
{{"index": 0, "is_useful": false}}

Chunks:
{numbered}
"""

    response = client.generate_content(prompt)
    raw = response.text.strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [{"index": i, "is_useful": False} for i in range(len(chunks))]


def extract_transcript(transcript_path: str, start_from: int = 0, batch_size: int = 20) -> str:
    """
    Takes a transcript JSON file path.
    Runs batch extraction on chunks.
    Saves useful chunks to a new JSON file.
    """
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    creator = transcript["creator"]
    chunks = transcript["chunks"][start_from:]

    print(f"Extracting from {len(chunks)} chunks for {creator} (starting at {start_from})...")

    useful_chunks = []

    for batch_start in range(0, len(chunks), batch_size):
        batch = chunks[batch_start:batch_start + batch_size]
        actual_index = start_from + batch_start

        print(f"Processing chunks {actual_index}–{actual_index + len(batch)}...")

        results = extract_batch(batch)

        for result in results:
            i = result.get("index", 0)
            if i >= len(batch):
                continue

            chunk = batch[i]

            if result.get("is_useful"):
                useful_chunks.append({
                    "creator": creator,
                    "start": chunk["start"],
                    "end": chunk["end"],
                    "timestamp_label": chunk["timestamp_label"],
                    "text": chunk["text"],
                    "category": result.get("category"),
                    "place_name": result.get("place_name"),
                    "cuisine_type": result.get("cuisine_type"),
                    "vibe": result.get("vibe"),
                    "summary": result.get("summary"),
                    "sentiment": result.get("sentiment")
                })
                print(f"  ✓ [{result.get('category')}] {result.get('summary')}")

    output = {
        "creator": creator,
        "audio_file": transcript["audio_file"],
        "total_chunks": len(transcript["chunks"]),
        "useful_chunks": len(useful_chunks),
        "chunks": useful_chunks
    }

    base_name = os.path.splitext(os.path.basename(transcript_path))[0]
    output_dir = os.path.dirname(transcript_path)
    output_path = os.path.join(output_dir, f"{base_name}_extracted.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(useful_chunks)}/{len(transcript['chunks'])} chunks were useful.")
    print(f"Saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    transcript_path = input("Path to transcript JSON: ")
    start = int(input("Start from chunk (0 for beginning): "))
    extract_transcript(transcript_path, start_from=start)
