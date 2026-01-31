import os
import librosa
import numpy as np
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Analyze_WAV")
root.geometry("500x300")        
root.resizable(False, False)

def count(folder):
    counter = 0
    for filename in os.listdir(folder):
        if filename.lower().endswith(".wav"):
            counter += 1
    return counter

def analyze_wav(file_path):
    y, sr = librosa.load(file_path, sr=None)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_index = np.argmax(chroma.mean(axis=1))
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = notes[key_index]

    return bpm, key

def rename_wavs_in_folder(folder, progress_bar, status_label, n):
    num = n
    for filename in os.listdir(folder):
        if filename.lower().endswith(".wav"):
            old_path = os.path.join(folder, filename)
            try:
                bpm, key = analyze_wav(old_path)
                BPM = int(round(bpm, 0))
                name, ext = os.path.splitext(filename)
                new_name = f"{name} | key; {key} | bpm; {BPM} |{ext}"
                new_path = os.path.join(folder, new_name)

                os.rename(old_path, new_path)
                print(f"{filename} -> {new_name} | BPM: {BPM} | Key: {key}")

            except Exception as e:
                print(f"ERROR with {filename}: {e}")
            num -= 1
            status_label.config(text=f"READY: {n - num} / {n}")
            progress_bar["value"] = 100 - (num / n * 100)
            status_label.update_idletasks()
            progress_bar.update_idletasks()

def start():
    n = count("downloads")
    progress["value"] = 0
    rename_wavs_in_folder("downloads", progress, status, n)

status = tk.Label(root, text="Status: ")
status.pack(pady=5)

progress = ttk.Progressbar(root, length=350, mode="determinate")
progress.pack(pady=5)

tk.Button(root, text="Start", command=start).pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
