
import sys
import subprocess
import os
from pathlib import Path

def download_instagram_video(insta_url, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Baixar o vídeo com instaloader
    try:
        subprocess.run([
            "instaloader",
            "--no-metadata-json",
            "--no-captions",
            "--dirname-pattern", str(output_dir),
            "--filename-pattern", "video",
            "--post-url", insta_url
        ], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: Failed to download Instagram video", file=sys.stderr)
        sys.exit(1)

    # Encontrar o arquivo .mp4 baixado
    video_files = list(output_dir.glob("**/video.mp4"))
    if not video_files:
        print("ERROR: No video file found after download", file=sys.stderr)
        sys.exit(1)
    video_path = video_files[0]

    # Converter para MP3
    mp3_path = video_path.with_suffix(".mp3")
    try:
        subprocess.run([
            "ffmpeg",
            "-i", str(video_path),
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "2",
            str(mp3_path)
        ], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: Failed to convert video to MP3", file=sys.stderr)
        sys.exit(1)

    print(mp3_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_instagram.py <instagram_url> <output_dir>", file=sys.stderr)
        sys.exit(1)

    instagram_url = sys.argv[1]
    output_directory = sys.argv[2]
    download_instagram_video(instagram_url, output_directory)
