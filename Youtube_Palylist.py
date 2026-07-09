#!/usr/bin/env python3
"""
YouTube Video Downloader - 1080p+ Only
Uses yt-dlp to download videos in 1080p or higher quality.

REQUIREMENT: ffmpeg must be installed to merge video+audio streams.
  - Windows: winget install ffmpeg
  - Or download from https://ffmpeg.org/download.html

Install Python dependency:
    pip install yt-dlp

Usage:
    python youtube_downloader.py
    python youtube_downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
    python youtube_downloader.py --url "URL" --output ./downloads
"""

import argparse
import os
import sys
import shutil

try:
    import yt_dlp
except ImportError:
    print("❌ yt-dlp is not installed.")
    print("   Run: pip install yt-dlp")
    sys.exit(1)


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available on the system PATH."""
    return shutil.which("ffmpeg") is not None


def download_video(url: str, output_dir: str = ".") -> None:
    """
    Download a YouTube video in 1080p or highest available quality above 1080p.
    Requires ffmpeg for merging separate video+audio streams.

    Args:
        url        : YouTube video or playlist URL
        output_dir : Directory to save the downloaded file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Format priority (1080p and above only):
    # 1. Try 4K (2160p)
    # 2. Try 1440p
    # 3. Try 1080p
    # 4. Fallback: best available (in case none of above exist)
    fmt = (
        "bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]"
        "/bestvideo[height>=1440][ext=mp4]+bestaudio[ext=m4a]"
        "/bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]"
        "/bestvideo[height>=1080]+bestaudio"
        "/best"
    )

    ydl_opts = {
        "outtmpl":              os.path.join(output_dir, "%(title)s [%(height)sp].%(ext)s"),
        "format":               fmt,
        "merge_output_format":  "mp4",
        "quiet":                False,
        "no_warnings":          True,
        "writethumbnail":       False,
        "postprocessors":       [],
    }

    print(f"\n🔗 URL      : {url}")
    print(f"📁 Output   : {os.path.abspath(output_dir)}")
    print(f"🎬 Quality  : 1080p or above (4K > 1440p > 1080p)\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info     = ydl.extract_info(url, download=False)
            title    = info.get("title", "Unknown")
            duration = info.get("duration", 0)
            uploader = info.get("uploader", "Unknown")
            height   = info.get("height") or "Unknown"

            print(f"📹 Title    : {title}")
            print(f"👤 Channel  : {uploader}")
            print(f"⏱  Duration : {duration // 60}m {duration % 60}s")
            print(f"📐 Selected : {height}p\n")

            # Warn if selected quality is below 1080p
            if isinstance(height, int) and height < 1080:
                print(f"⚠️  Warning  : Best available quality is only {height}p (1080p not available for this video)\n")

            confirm = input("Start download? [Y/n]: ").strip().lower()
            if confirm in ("n", "no"):
                print("Download cancelled.")
                return

            ydl.download([url])
            print("\n✅ Download complete!")

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Download failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user.")
        sys.exit(0)


def list_formats(url: str) -> None:
    """List all available formats for a given URL."""
    ydl_opts = {"listformats": True, "quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Error fetching formats: {e}")
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube videos in 1080p or higher quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_downloader.py
  python youtube_downloader.py --url "https://youtu.be/VIDEO_ID"
  python youtube_downloader.py --url "URL" --output ./videos
  python youtube_downloader.py --url "URL" --list-formats
        """,
    )
    parser.add_argument("--url",  "-u",  type=str, help="YouTube video URL")
    parser.add_argument("--output", "-o", type=str, default="./downloads",
                        help="Output directory (default: ./downloads)")
    parser.add_argument("--list-formats", "-lf", action="store_true",
                        help="List all available formats for the URL and exit")
    return parser.parse_args()


def main() -> None:
    # Check ffmpeg before doing anything
    if not check_ffmpeg():
        print("❌ ffmpeg is not installed or not found in PATH.")
        print("   1080p+ requires ffmpeg to merge video and audio streams.")
        print("\n   Install ffmpeg:")
        print("   → Windows : winget install ffmpeg")
        print("   → Download: https://ffmpeg.org/download.html")
        print("   → After install, restart your terminal and try again.\n")
        sys.exit(1)

    args = parse_args()

    url = args.url
    if not url:
        url = input("Enter YouTube URL: ").strip()
        if not url:
            print("❌ No URL provided. Exiting.")
            sys.exit(1)

    if args.list_formats:
        list_formats(url)
        return

    download_video(url=url, output_dir=args.output)


# Run directly
main()