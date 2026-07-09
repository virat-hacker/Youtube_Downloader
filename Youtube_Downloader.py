#!/usr/bin/env python3
"""
YouTube Video Downloader — 1080p and above
--------------------------------------------
Downloads YouTube videos, only picking video formats that are
1080p (1920x1080) or higher resolution, merged with the best
available audio track.

Requirements:
    pip install yt-dlp
    ffmpeg installed and available on PATH (needed to merge video+audio)

Usage:
    python youtube_downloader_1080p.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
    python youtube_downloader_1080p.py "URL1" "URL2" "URL3"
    python youtube_downloader_1080p.py --output "D:/Videos" "URL"
"""

import argparse
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Install it with:\n    pip install yt-dlp")
    sys.exit(1)


def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\rDownloading... {percent} at {speed}, ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print("\nDownload finished, now merging/post-processing...")


def build_options(output_dir: str, min_height: int = 1080) -> dict:
    """
    Format selector explanation:
    - bestvideo[height>=1080] : best video stream that is 1080p or higher
    - +bestaudio               : merged with the best audio stream
    - /best[height>=1080]      : fallback for pre-merged formats >=1080p
    This ensures we NEVER silently fall back to something below 1080p.
    """
    output_template = str(Path(output_dir) / "%(title)s [%(height)sp].%(ext)s")

    return {
        "format": f"bestvideo[height>={min_height}]+bestaudio/best[height>={min_height}]",
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "noplaylist": True,
        "progress_hooks": [progress_hook],
        "quiet": False,
        "no_warnings": False,
        # Fail loudly instead of silently grabbing a lower-res format
        "format_sort": ["res:2160", "res:1440", "res:1080"],
    }


def download_video(url: str, ydl_opts: dict) -> bool:
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            height = info.get("height", 0)

            if height and height < 1080:
                print(f"Skipping '{info.get('title')}': "
                      f"highest available resolution is only {height}p (below 1080p).")
                return False

            print(f"Found: {info.get('title')} — downloading at "
                  f"{height or 'unknown'}p...")
            ydl.download([url])
            print(f"Saved: {info.get('title')}\n")
            return True

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading {url}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos in 1080p or higher quality."
    )
    parser.add_argument("urls", nargs="+", help="One or more YouTube video URLs")
    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="Output directory (default: ./downloads)"
    )
    parser.add_argument(
        "--min-height",
        type=int,
        default=1080,
        help="Minimum vertical resolution to accept (default: 1080)"
    )
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)
    ydl_opts = build_options(args.output, args.min_height)

    success_count = 0
    for url in args.urls:
        if download_video(url, ydl_opts):
            success_count += 1

    print(f"\nDone: {success_count}/{len(args.urls)} video(s) downloaded successfully.")


if __name__ == "__main__":
    main()