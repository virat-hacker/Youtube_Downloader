#!/usr/bin/env python3
import os
import sys
import threading
import shutil
import customtkinter as ctk
import yt_dlp

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class YoutubeDownloaderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ Interactive YouTube Downloader")
        self.geometry("720x560")
        self.resizable(False, False)

        # Configure Grid Rows to force strict spacing layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Title Header Banner
        self.title_label = ctk.CTkLabel(self, text="YouTube Video & Playlist Downloader",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="nsew")

        # --- URL INPUT SECTION ---
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.url_label = ctk.CTkLabel(self.url_frame, text="Paste YouTube URL:", font=ctk.CTkFont(weight="bold"))
        self.url_label.pack(anchor="w", padx=15, pady=(5, 2))

        self.url_entry = ctk.CTkEntry(self.url_frame,
                                      placeholder_text="https://www.youtube.com/playlist?list=... or Video Link",
                                      width=640)
        self.url_entry.pack(padx=15, pady=(0, 10), fill="x")

        # --- SETTINGS ROW ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.qual_label = ctk.CTkLabel(self.settings_frame, text="Target Max Quality:", font=ctk.CTkFont(weight="bold"))
        self.qual_label.grid(row=0, column=0, padx=15, pady=(5, 2), sticky="w")

        self.qual_dropdown = ctk.CTkComboBox(self.settings_frame,
                                             values=["Best Available", "2160p (4K)", "1440p (2K)", "1080p", "720p",
                                                     "480p"], width=160)
        self.qual_dropdown.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")
        self.qual_dropdown.set("1080p")

        self.path_label = ctk.CTkLabel(self.settings_frame, text="Save Destination Folder:",
                                       font=ctk.CTkFont(weight="bold"))
        self.path_label.grid(row=0, column=1, padx=15, pady=(5, 2), sticky="w")

        self.path_entry = ctk.CTkEntry(self.settings_frame, width=320)
        self.path_entry.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="w")
        self.path_entry.insert(0, os.path.abspath("./downloads"))

        self.browse_btn = ctk.CTkButton(self.settings_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_btn.grid(row=1, column=2, padx=(0, 15), pady=(0, 10))

        # --- TERMINAL FEEDBACK LOG ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.log_box = ctk.CTkTextbox(self.log_frame, state="disabled", wrap="word", fg_color="#1E1E1E",
                                      text_color="#A9FFB2", height=140)
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)

        # --- DYNAMIC PROGRESS STATUS LABEL ---
        self.status_label = ctk.CTkLabel(self, text="Status: Ready to Download",
                                         font=ctk.CTkFont(size=12, weight="bold"), text_color="yellow")
        self.status_label.grid(row=4, column=0, padx=20, pady=2, sticky="ew")

        # --- EXECUTION BUTTON ---
        self.download_btn = ctk.CTkButton(self, text="🚀 START DOWNLOAD", font=ctk.CTkFont(size=16, weight="bold"),
                                          height=42, command=self.start_download_thread)
        self.download_btn.grid(row=5, column=0, padx=20, pady=(5, 15), sticky="ew")

    def browse_folder(self):
        selected_dir = ctk.filedialog.askdirectory(initialdir=self.path_entry.get())
        if selected_dir:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, os.path.abspath(selected_dir))

    def write_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_idletasks()

    def update_status(self, text, color="white"):
        self.status_label.configure(text=f"Status: {text}", text_color=color)
        self.update_idletasks()

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.write_log("❌ Error: Please input a valid YouTube URL first.")
            return

        self.download_btn.configure(state="disabled", text="⚡ DOWNLOADING...")
        self.update_status("Processing video tracking pipelines...", "yellow")

        threading.Thread(target=self.execute_download, args=(url,), daemon=True).start()

    def execute_download(self, url):
        output_dir = self.path_entry.get().strip()
        quality_sel = self.qual_dropdown.get()
        os.makedirs(output_dir, exist_ok=True)

        # --- REMOVED STRICT FORMAT RESTRICTIONS ---
        # Now it targets the absolute best audio and video streams for the target resolution, regardless of container (mp4 vs webm).
        if quality_sel == "Best Available":
            fmt = "bestvideo+bestaudio/best"
        else:
            res = quality_sel.split("p")[0]
            fmt = f"bestvideo[height<={res}]+bestaudio/best[height<={res}]/best"

        def logger_hook(d):
            if d['status'] == 'downloading':
                pct = d.get('_percent_str', '0%').strip()
                eta = d.get('_eta_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                self.update_status(f"Downloading: {pct} | Speed: {speed} | ETA: {eta}", "#3B9CFF")
            elif d['status'] == 'finished':
                self.update_status("Merging Audio/Video streams via ffmpeg...", "orange")

        ydl_opts = {
            "outtmpl": os.path.join(output_dir, "%(playlist_title)s",
                                    "%(playlist_index)02d_%(title)s.%(ext)s") if "list=" in url else os.path.join(
                output_dir, "%(title)s.%(ext)s"),
            "format": fmt,
            # This line forces ffmpeg to save the final output file strictly as a clean .mp4
            "merge_output_format": "mp4",
            "progress_hooks": [logger_hook],
            "quiet": True,
            "no_warnings": True,
            "rm_cachedir": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.write_log(f"🔗 Analyzing Link: {url}")
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "YouTube Target")
                self.write_log(f"✅ Finished: '{title}'")
                self.update_status("Download Complete Successfully!", "green")
        except Exception as e:
            self.write_log(f"❌ Error: {str(e)}")
            self.update_status("Failed with errors.", "red")
        finally:
            self.download_btn.configure(state="normal", text="🚀 START DOWNLOAD")


if __name__ == "__main__":
    app = YoutubeDownloaderGUI()
    app.mainloop()