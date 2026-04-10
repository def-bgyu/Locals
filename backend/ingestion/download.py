import yt_dlp
import os

def download_audio(url: str, creator_name: str) -> str:
    """
    Takes a YouTube URL and a creator name.
    Downloads the audio and saves it to data/audio/.
    Returns the file path of the downloaded audio.
    """

    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "audio")
    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, f"{creator_name}_%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "unknown")
        file_path = os.path.join(output_dir, f"{creator_name}_{title}.mp3")

    print(f"Downloaded: {title}")
    print(f"Saved to: {file_path}")

    return file_path


if __name__ == "__main__":
    url = input("Paste a YouTube URL: ")
    creator = input("Creator name (no spaces, e.g. emma_chen): ")
    download_audio(url, creator)