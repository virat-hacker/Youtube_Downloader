# 📺 YouTube Downloader Suite

A collection of Python scripts to download YouTube videos in **1080p or higher quality**. Includes both CLI and GUI options for single videos and entire playlists.

---

## ✨ Features

- **1080p+ Quality Enforcement** — Only downloads videos at 1080p, 1440p, or 4K resolution
- **Multiple Download Modes**:
  - Batch CLI downloader for multiple URLs
  - Interactive CLI with confirmation prompts
  - Full-featured GUI with real-time progress
- **Playlist Support** — Download entire playlists with proper naming
- **Smart Merging** — Automatically merges separate video + audio streams via `ffmpeg`
- **Live Progress** — Real-time download speed, percentage, and ETA

---

## 📁 File Structure

```
├── Youtube_Downloader.py          # CLI: Batch download multiple URLs (1080p+)
├── Youtube_Palylist.py            # CLI: Interactive single video/playlist downloader
├── Youtube_Playlis_Downloader.py  # GUI: Full visual downloader with settings
└── README.md
```

---

## 📋 Prerequisites

| Dependency | Purpose | Installation |
|------------|---------|--------------|
| **Python 3.8+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **yt-dlp** | YouTube extraction | `pip install yt-dlp` |
| **ffmpeg** | Merge video + audio streams | See below |
| **customtkinter** *(GUI only)* | GUI framework | `pip install customtkinter` |

### Installing FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update && sudo apt install ffmpeg
```

> ⚠️ After installing ffmpeg, **restart your terminal** to ensure it's available on PATH.

---

## 🚀 Installation

```bash
# Clone or download the scripts
git clone https://github.com/YOUR_USERNAME/Youtube-Downloader-Suite.git
cd Youtube-Downloader-Suite

# Install Python dependencies
pip install yt-dlp customtkinter
```

---

## 📖 Usage

### 1. `Youtube_Downloader.py` — Batch CLI Downloader

Downloads multiple videos in 1080p+ without any prompts. Ideal for scripting.

```bash
# Download a single video
python Youtube_Downloader.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"

# Download multiple videos at once
python Youtube_Downloader.py "URL1" "URL2" "URL3"

# Specify output directory
python Youtube_Downloader.py --output "D:/Videos" "URL"

# Set custom minimum resolution (e.g., only 4K)
python Youtube_Downloader.py --min-height 2160 "URL"
```

**Output filename format:**
```
Video Title [1080p].mp4
```

---

### 2. `Youtube_Palylist.py` — Interactive CLI Downloader

Prompts you with video details before downloading. Supports format listing.

```bash
# Run and enter URL interactively
python Youtube_Palylist.py

# Pass URL directly
python Youtube_Palylist.py --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Specify output folder
python Youtube_Palylist.py --url "URL" --output ./my_videos

# List all available formats (no download)
python Youtube_Palylist.py --url "URL" --list-formats
```

**Example interaction:**
```
🔗 URL      : https://www.youtube.com/watch?v=dQw4w9WgXcQ
📁 Output   : C:\Users\You\downloads
🎬 Quality  : 1080p or above (4K > 1440p > 1080p)

📹 Title    : Rick Astley - Never Gonna Give You Up
👤 Channel  : Rick Astley
⏱  Duration : 3m 33s
📐 Selected : 1080p

Start download? [Y/n]: y
✅ Download complete!
```

---

### 3. `Youtube_Playlis_Downloader.py` — GUI Downloader

A visual interface built with CustomTkinter. Best for non-technical users.

```bash
python Youtube_Playlis_Downloader.py
```

**GUI Features:**
| Control | Description |
|---------|-------------|
| **URL Input** | Paste any YouTube video or playlist link |
| **Quality Dropdown** | Best Available, 4K, 1440p, 1080p, 720p, 480p |
| **Browse Button** | Select save destination folder |
| **Log Console** | Real-time download log with color-coded output |
| **Status Bar** | Live progress: percentage, speed, ETA |

**Playlist Output Structure:**
```
downloads/
└── Playlist Name/
    ├── 01_First Video.mp4
    ├── 02_Second Video.mp4
    └── 03_Third Video.mp4
```

---

## ⚙️ Quality Behavior

| Script | Default Behavior | Below 1080p |
|--------|-----------------|-------------|
| `Youtube_Downloader.py` | Strictly **1080p+ only** | ⛔ Skips with warning |
| `Youtube_Palylist.py` | Prioritizes 1080p+ | ⚠️ Warns, then downloads best available |
| `Youtube_Playlis_Downloader.py` | Targets selected quality | ✅ Falls back to best available |

---

## 🔧 Common Issues

### `yt-dlp is not installed`
```bash
pip install yt-dlp
```

### `ffmpeg is not found`
Ensure ffmpeg is installed and on your system PATH. Restart your terminal after installation.

### Video downloads but has no audio
This means ffmpeg is not working correctly. Reinstall ffmpeg and verify:
```bash
ffmpeg -version
```

### `Unavailable format` error
Some videos don't have 1080p+ available. Use `Youtube_Palylist.py` with `--list-formats` to see all available formats.

---

## 📄 License

This project is provided as-is for personal and educational use. Please respect YouTube's Terms of Service and copyright laws.

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube download library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern GUI framework
- [FFmpeg](https://ffmpeg.org/) — Multimedia processing
