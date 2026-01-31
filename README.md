DJ Tools – Free Python Scripts

for Linux: 
pip install yt-dlp librosa numpy
sudo apt install ffmpeg

for Windows:
pip install yt-dlp librosa numpy
ffmpeg -version (if u get error google it)


These are simple Python scripts for DJs on a budget.
They are mostly working, though not fully error-proof yet.

'''---yt_to_wav.py---'''

A simple GUI application to download music from YouTube as WAV files.

WAV files are not truly lossless — converting from YouTube’s WebM/Opus or AAC format always involves some data loss.
On first run, it creates a downloads folder where all files will be saved. Do not rename this folder if you plan to use other scripts in this suite.
How it works: paste a YouTube URL and click Download.
Bonus: if you copy a new link and press DEL/PASTE, it automatically replaces the previous URL.

'''---find_key_bpm.py---'''

Analyzes WAV files in the downloads folder for key and BPM.

The detection is not perfect but gives a reasonably good estimate for DJing purposes.
The script automatically appends the key and BPM info to the file name.
