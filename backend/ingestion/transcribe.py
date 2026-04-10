import json
import os
from faster_whisper import WhisperModel

def transcribe_audio(file_path: str, creator_name: str) -> str:
    """
    Takes an audio file path and creator name.
    Transcribes the audio into timestamped chunks.
    Saves the transcript as JSON and returns the output path.
    """

    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "transcripts")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading Whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print(f"Transcribing {file_path}...")
    segments, info = model.transcribe(file_path, beam_size=5)

    print(f"Detected language: {info.language}")

    chunks = []
    for segment in segments:
        chunk = {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip(),
            "timestamp_label": format_timestamp(segment.start)
        }
        chunks.append(chunk)
        print(f"[{chunk['timestamp_label']}] {chunk['text']}")

    transcript_data = {
        "creator": creator_name,
        "audio_file": file_path,
        "language": info.language,
        "chunks": chunks
    }

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)

    print(f"\nTranscript saved to: {output_path}")
    print(f"Total chunks: {len(chunks)}")

    return output_path


def format_timestamp(seconds: float) -> str:
    """Converts seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    file_path = input("Path to audio file: ")
    creator = input("Creator name: ")
    transcribe_audio(file_path, creator)