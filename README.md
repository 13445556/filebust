🧠 FileBust – All-in-One File Optimizer & Transcoder
⚡ Smart. Fast. Space-Saving. Cross-Platform.

“FileBust: because every megabyte matters.”

📸 1. Project Overview

FileBust is a single-command media optimizer that compresses and transcodes your files — audio, video, and images — using ffmpeg, pillow, and mutagen.
It’s designed for developers, editors, and creators who want maximum compression with zero quality loss.

🧩 2. Key Features

✅ Auto-detects file type (image/audio/video)
✅ Converts to modern, smaller formats (webp, opus, mp4)
✅ Intelligent renaming to prevent overwrite
✅ File size comparison before/after
✅ Recursive folder scanning
✅ Progress updates and summary stats
✅ Built-in error handling
✅ Single-line CLI execution

🧱 3. Installation & Setup
🧰 Requirements

Python 3.10+

FFmpeg (add to PATH)

Pip packages:

pip install pillow mutagen tqdm colorama

🪶 Clone the Repo
git clone https://github.com/<your-username>/filebust.git
cd filebust

🧩 4. How to Run
🧭 Basic Usage

Optimize all supported files inside a folder:

python f3.py "path/to/folder"

⚙️ Transcode Mode

Transcode all media (video, audio, and images) into optimized modern formats:

python f3.py "path/to/folder" --transcode

💾 Example Output
ℹ️ 🎬 Transcoding Video: demo.mp4
ℹ️ ✅ demo.mp4: 50.0MB → 28.2MB (43.6% saved)
ℹ️ 🎬 Transcoding Image: logo.png
ℹ️ ✅ logo.png: 2.0MB → 48.7KB (97.6% saved)

⚡ 5. Demo in One Command

All-in-One Demo Command (for presentation):

python f3.py "samples" --transcode


This will:

Scan all files in /samples

Compress and transcode supported media

Display before/after sizes

Print total savings in the console

📊 6. Supported File Types
Type	Input Formats	Output Format	Compression Tool
🎬 Video	.mp4 .mkv .mov	.mp4	FFmpeg (libx264)
🎵 Audio	.mp3 .wav .flac	.opus	FFmpeg (libopus)
🖼️ Image	.jpg .jpeg .png	.webp	Pillow / FFmpeg
🚀 7. Output Example
ℹ️ 🎬 Transcoding Audio: 5-MB-MP3.mp3
ℹ️ ✅ 5-MB-MP3.mp3: 5.0MB → 2.6MB (47.8% saved)
ℹ️ 🎬 Transcoding Image: sample.png
ℹ️ ✅ sample.png: 2.0MB → 45.0KB (97.7% saved)

🧠 8. Constraints & Notes

Works on Windows, macOS, and Linux

Requires FFmpeg in system PATH

Skips already optimized files (_opt suffix)

Non-media files are ignored

Safe: original files are preserved

🧩 9. File Structure
filebust/
│
├── f3.py               # Main script
├── README.md           # Documentation
├── samples/            # Test media folder
└── requirements.txt    # Dependency list

🧠 10. Author & Credits

👨‍💻 Vedant gupta
🎯 Project for Code Olympics 2025

💬 11. Tagline for Demo

“From 100MB to 10MB in seconds — powered by FileBust.”
