# 🧠 **FileBust Command Reference**

## 🪄 1️⃣  Clone the Repository

```bash
git clone https://github.com/<your-username>/filebust.git
cd filebust
```

---

## 🧱 2️⃣  Install Requirements

### 🧰 Install Python Libraries

```bash
pip install pillow mutagen tqdm colorama
```

### 🎞️ Install FFmpeg (required for transcoding)

#### 🪟 Windows:

Download from 👉 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
Then add `ffmpeg/bin` to your **PATH** environment variable.

#### 🐧 Linux / macOS:

```bash
sudo apt install ffmpeg       # Ubuntu / Debian
# or
brew install ffmpeg           # macOS
```

---

## 🧩 3️⃣  Run the Optimizer

### 🎬 Basic Folder Optimization

Process and optimize all files in a folder (non-destructive):

```bash
python f3.py "path/to/folder"
```

---

### ⚙️ Transcode Media Files

Convert videos, images, and audio to smaller modern formats:

```bash
python f3.py "path/to/folder" --transcode
```

---

### 🎚️ Set Quality Levels

Choose between three compression qualities:

```bash
python f3.py "path/to/folder" --transcode --quality low
python f3.py "path/to/folder" --transcode --quality medium
python f3.py "path/to/folder" --transcode --quality high
```

Default = `medium`

---

### 🧼 Deduplicate Files

Removes duplicate files safely based on file hashes:

```bash
python f3.py "path/to/folder" --dedup
```

---

### 🗂️ Organize Files

Automatically sort files into folders by **type** or **size**:

```bash
python f3.py "path/to/folder" --organize type
python f3.py "path/to/folder" --organize size
```

---

### ⚡ Run Everything (All-in-One Command)

Use this in your **presentation demo** 👇
It performs deduplication, organization, and transcoding together:

```bash
python f3.py "samples" --dedup --organize type --transcode --quality medium --threads 4 --verbose
```

That’s your **hero command** 🎥 — the one to show during your **3–4 minute video**.

---

## 🧮 4️⃣  Example Outputs

### Successful Transcode:

```
🎬 Transcoding Video: travel.mp4
✅ travel.mp4: 80.5MB → 45.2MB (43.8% saved)
```

### Duplicate Removal:

```
🗑️ Removed duplicate: sunset_1.jpg
```

### Organization:

```
📂 Moved: logo.png → png/
```

### Summary:

```
🎉 Summary: 6 files | Saved: 180.3MB (58.2%) | Errors: 0
```

---

## 🧠 5️⃣  Troubleshooting

| Issue                     | Cause                               | Fix                                            |
| ------------------------- | ----------------------------------- | ---------------------------------------------- |
| `Tool not found: ffmpeg`  | FFmpeg not installed or not in PATH | Install FFmpeg and restart terminal            |
| `Permission denied`       | Folder is read-only                 | Run as admin or choose another folder          |
| `Output file not created` | File type not supported             | Use supported formats (.mp4, .jpg, .mp3, etc.) |

---

## 💡 6️⃣  Clean Exit

If you stop midway:

```bash
CTRL + C
```

The script safely exits and prints summary stats.

---

## 🎯 7️⃣  Optional Developer Commands

### Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### Save dependencies to requirements.txt

```bash
pip freeze > requirements.txt
```

### Run code linter (optional)

```bash
flake8 f3.py --max-line-length=200
```

---

## 🧾 8️⃣  For Presentation (Sequence Plan)

1️⃣ Show challenge image (“Error-Proof Coder + File Management + 200 lines”)
2️⃣ Show GitHub repo (`README.md` with usage + command list)
3️⃣ Explain libraries installed (`ffmpeg`, `pillow`, `mutagen`, etc.)
4️⃣ Run your **All-in-One Command** live:

```bash
python f3.py "samples" --dedup --organize type --transcode --quality medium --threads 4 --verbose
```

5️⃣ Show results (before/after sizes)
6️⃣ End with your tagline:

> “From 100MB to 10MB — safely, smartly, instantly. That’s FileBust.”

It’ll sound like an energetic presentation with timing cues (e.g., “pause 2s”, “zoom in on terminal output”).
