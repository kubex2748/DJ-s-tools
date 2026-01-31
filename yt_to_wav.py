import tkinter as tk
from tkinter import ttk
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import threading

root = tk.Tk()
root.title("Download_yt_to_WAV")
root.geometry("500x300")        
root.resizable(False, False)

def download_yt_to_wav(url, progress_bar, status_label, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    title = ""
    try:
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and 'downloaded_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                    progress_bar["value"] = percent
                    status_label.config(text=f"downloading... {percent:.1f}%")
                    root.update_idletasks()

            elif d['status'] == 'finished':
                status_label.config(text="convert to WAV...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'postprocessor_args': [
                '-ar', '48000',
                '-ac', '2',
                '-sample_fmt', 's16'
            ],
            'noplaylist': True,
            'quiet': False,
            'keepvideo': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'unknown_title')

        progress_bar["value"] = 100
        status_label.config(text=f"{title} -> READY ✅")
    except DownloadError:
        progress_bar["value"] = 0
        status_label.config(text="URL dosen't exist")
    except FileNotFoundError:
        progress_bar["value"] = 0
        status_label.config(text="no FFmpeg in system")
    except Exception as e:
        progress_bar["value"] = 0
        status_label.config(text=f"ERROR: {str(e)[:50]}")

def start_download():
    url = entry.get()
    progress["value"] = 0
    status.config(text="Start...")

    thread = threading.Thread(
        target=download_yt_to_wav,
        args=(url, progress, status),
        daemon=True
    )
    thread.start()

def del_paste():
    entry.delete(0, tk.END)
    entry.insert(0, root.clipboard_get())
    entry.pack()

tk.Label(root, text="URL:").pack(pady=5)

entry = tk.Entry(root, width=60)
entry.pack()

status = tk.Label(root, text="Status: ")
status.pack(pady=5)

progress = ttk.Progressbar(root, length=350, mode="determinate")
progress.pack(pady=5)

tk.Button(root, text="Download", command=start_download).pack(pady=5)
tk.Button(root, text="DEL/PASTE", command=del_paste).pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
