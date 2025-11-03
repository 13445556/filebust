#!/usr/bin/env python3
"""Error-Proof Media Optimizer - Thread-safe parallel processing"""
import os, sys, argparse, subprocess, shutil, hashlib
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
class MediaOptimizer:
    """Single-function master class for media optimization"""
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {"processed": 0, "errors": 0, "old_size": 0, "new_size": 0}
        self.lock = Lock()  # Thread-safe stats updates
    def log(self, msg: str, error: bool = False):
        """Thread-safe logging with error tracking"""
        print(f"{'⚠️' if error else 'ℹ️'} {msg}")
        if error:
            with self.lock:
                self.stats["errors"] += 1
    def safe_hash(self, path: Path) -> Optional[str]:
        """Calculate file hash with error handling"""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            self.log(f"Hash failed for {path.name}: {e}", error=True)
            return None
    def safe_run(self, cmd: list) -> bool:
        """Execute command with comprehensive error handling"""
        try:
            if self.verbose: self.log(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
            return True
        except subprocess.TimeoutExpired:
            self.log(f"Command timeout: {cmd[0]}", error=True)
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e.stderr[:100]}", error=True)
        except FileNotFoundError:
            self.log(f"Tool not found: {cmd[0]} - install ffmpeg!", error=True)
        except Exception as e:
            self.log(f"Unexpected error: {type(e).__name__}: {e}", error=True)
        return False
    def human_size(self, size: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0: return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}PB"
    def transcode(self, src: Path, quality: str = "medium") -> Optional[Path]:
        """Transcode media with full error handling"""
        if not src.exists() or not src.is_file():
            self.log(f"Invalid source: {src}", error=True)
            return None
        ext = src.suffix.lower()
        qmap = {"low": 32, "medium": 28, "high": 23}
        crf = qmap.get(quality, 28)
        # Determine output format and command
        config = {
            "video": ([".mp4", ".mkv", ".avi", ".mov", ".webm"], ".mp4", 
                     ["ffmpeg", "-y", "-i", str(src), "-c:v", "libx265", "-preset", "medium", 
                      "-crf", str(crf), "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"]),
            "audio": ([".mp3", ".wav", ".aac", ".flac", ".m4a"], ".opus",
                     ["ffmpeg", "-y", "-i", str(src), "-c:a", "libopus", "-b:a", "96k"]),
            "image": ([".jpg", ".jpeg", ".png", ".bmp"], ".webp",
                     ["ffmpeg", "-y", "-i", str(src), "-c:v", "libwebp", "-q:v", 
                      {"low": "70", "medium": "80", "high": "90"}[quality]])
        }
        media_type = dst = cmd = None
        for mtype, (exts, out_ext, base_cmd) in config.items():
            if ext in exts:
                media_type = mtype.capitalize()
                dst = src.with_stem(f"{src.stem}_opt").with_suffix(out_ext)
                cmd = base_cmd + [str(dst)]
                break
        if not cmd: return None
        try:
            old_size = src.stat().st_size
            self.log(f"🎬 Transcoding {media_type}: {src.name}")
            if not self.safe_run(cmd): return None
            if not dst.exists():
                self.log(f"Output file not created: {dst}", error=True)
                return None
            new_size = dst.stat().st_size
            
            # Only keep if smaller
            if new_size >= old_size:
                self.log(f"⏩ Skipped (no savings): {src.name}")
                dst.unlink(missing_ok=True)
                return None
            
            saved = old_size - new_size
            pct = (saved / old_size * 100)
            self.log(f"✅ {src.name}: {self.human_size(old_size)} → {self.human_size(new_size)} ({pct:.1f}% saved)")
            
            # Thread-safe stats update
            with self.lock:
                self.stats["old_size"] += old_size
                self.stats["new_size"] += new_size
                self.stats["processed"] += 1
            # Delete original after successful, smaller transcode
            try:
                src.unlink()
            except OSError as e:
                self.log(f"Failed to remove original {src.name}: {e}", error=True)
            return dst
            
        except Exception as e:
            self.log(f"Transcode failed for {src.name}: {e}", error=True)
            if dst and dst.exists(): dst.unlink(missing_ok=True)
            return None
    
    def deduplicate(self, folder: Path) -> int:
        """Remove duplicate files safely"""
        seen, removed = {}, 0
        try:
            for f in sorted(folder.rglob("*")):
                if not f.is_file(): continue
                h = self.safe_hash(f)
                if not h: continue
                if h in seen:
                    try:
                        f.unlink()
                        self.log(f"🗑️ Removed duplicate: {f.name}")
                        removed += 1
                    except OSError as e:
                        self.log(f"Failed to remove {f.name}: {e}", error=True)
                else:
                    seen[h] = f
        except Exception as e:
            self.log(f"Deduplication error: {e}", error=True)
        return removed
    
    def organize(self, folder: Path, mode: str = "type") -> int:
        """Organize files by type/size with error handling"""
        moved = 0
        try:
            for f in sorted(folder.rglob("*")):
                if not f.is_file(): continue         
                target_dir = folder / ((f.suffix.lower()[1:] or "noext") if mode == "type" 
                                      else f"{f.stat().st_size // (1024 * 1024)}MB")        
                if f.parent == target_dir: continue       
                try:
                    target_dir.mkdir(exist_ok=True, parents=True)
                    shutil.move(str(f), target_dir / f.name)
                    self.log(f"📂 Moved: {f.name} → {target_dir.name}")
                    moved += 1
                except (OSError, shutil.Error) as e:
                    self.log(f"Move failed for {f.name}: {e}", error=True)
        except Exception as e:
            self.log(f"Organization error: {e}", error=True)
        return moved
def main():
    p = argparse.ArgumentParser(description="Error-Proof Media Optimizer")
    p.add_argument("folder", help="Target folder")
    p.add_argument("--transcode", action="store_true", help="Transcode media files")
    p.add_argument("--quality", choices=["low", "medium", "high"], default="medium")
    p.add_argument("--dedup", action="store_true", help="Remove duplicates")
    p.add_argument("--organize", choices=["type", "size"], help="Organize files")
    p.add_argument("--threads", type=int, default=4, help="Parallel workers (default: 4)")
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    args = p.parse_args()
    folder = Path(args.folder)
    if not folder.exists() or not folder.is_dir(): sys.exit("❌ Invalid folder path!")
    optimizer = MediaOptimizer(verbose=args.verbose)
    try:
        if args.dedup:
            removed = optimizer.deduplicate(folder)
            print(f"\n✨ Removed {removed} duplicates")
        
        if args.organize:
            moved = optimizer.organize(folder, args.organize)
            print(f"\n✨ Organized {moved} files")
        
        if args.transcode:
            files = [f for f in folder.rglob("*") if f.is_file()]
            with ThreadPoolExecutor(max_workers=args.threads) as ex:
                list(ex.map(lambda f: optimizer.transcode(f, args.quality), files))
            
            if optimizer.stats["processed"] > 0:
                saved = optimizer.stats["old_size"] - optimizer.stats["new_size"]
                pct = (saved / optimizer.stats["old_size"] * 100)
                print(f"\n🎉 Summary: {optimizer.stats['processed']} files | "
                      f"Saved: {optimizer.human_size(saved)} ({pct:.1f}%) | "
                      f"Errors: {optimizer.stats['errors']}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__": main()