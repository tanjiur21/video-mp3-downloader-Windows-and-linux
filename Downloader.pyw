import os
import sys
import time
import threading
import subprocess
import importlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

SAVE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "MyDownloads")

OPTIONS = {
    "🎵 MP3 Song - Good (320kbps)": ("mp3", "320"),
    "🎵 MP3 Song - Medium (192kbps)": ("mp3", "192"),
    "🎬 Video - Max": ("video", "best"),
    "🎬 Video - 1080p": ("video", "1080"),
    "🎬 Video - 720p": ("video", "720"),
    "🎬 Video - 480p (Low Data)": ("video", "480"),
}

FFMPEG_PATH = None
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".mp3_downloader_folder")


def load_save_dir():
    """Return the last folder the user chose (or the default one)."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            path = f.read().strip()
        if path:
            return path
    except OSError:
        pass
    return SAVE_DIR


def store_save_dir(path):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(path)
    except OSError:
        pass


def pip_install(*packages):
    flags = 0x08000000 if os.name == "nt" else 0  # remove the black window
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-U", "--disable-pip-version-check",
         "--timeout", "15", *packages],
        creationflags=flags,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def setup_dependencies():
    global FFMPEG_PATH

    # Update yt-dlp once a day (silently skipped if offline)
    stamp = os.path.join(os.path.expanduser("~"), ".mp3_downloader_last_update")
    try:
        due = time.time() - os.path.getmtime(stamp) > 86400
    except OSError:
        due = True
    if due:
        try:
            pip_install("yt-dlp")
            with open(stamp, "w"):
                pass
            importlib.invalidate_caches()
        except Exception:
            pass

    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        pip_install("yt-dlp")
        importlib.invalidate_caches()
    try:
        import imageio_ffmpeg
    except ImportError:
        pip_install("imageio-ffmpeg")
        importlib.invalidate_caches()
        import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


class App:
    def __init__(self, root):
        self.root = root
        root.title("Video / MP3 Downloader--->tanjiur21")
        root.geometry("560x400")
        root.resizable(False, False)

        self.save_dir = load_save_dir()
        self.dir_var = tk.StringVar(value=self.save_dir)

        pad = {"padx": 18}

        ttk.Label(root, text="Drop your link here:",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(16, 4), **pad)

        row = ttk.Frame(root)
        row.pack(fill="x", **pad)
        self.url_var = tk.StringVar()
        self.entry = ttk.Entry(row, textvariable=self.url_var, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=4)
        ttk.Button(row, text="📋 Paste", command=self.paste).pack(side="left", padx=(8, 0))

        ttk.Label(root, text="What you want to Download?",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 4), **pad)
        self.choice = ttk.Combobox(root, values=list(OPTIONS.keys()),
                                   state="readonly", font=("Segoe UI", 11))
        self.choice.current(0)
        self.choice.pack(fill="x", **pad)

        ttk.Label(root, text="Save to (folder):",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 4), **pad)
        row2 = ttk.Frame(root)
        row2.pack(fill="x", **pad)
        ttk.Entry(row2, textvariable=self.dir_var, state="readonly",
                  font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True, ipady=3)
        ttk.Button(row2, text="📁 Browse", command=self.browse).pack(side="left", padx=(8, 0))

        self.btn = ttk.Button(root, text="⬇  Download", command=self.start, state="disabled")
        self.btn.pack(fill="x", pady=(18, 8), ipady=8, **pad)

        self.progress = ttk.Progressbar(root, mode="determinate", maximum=100)
        self.progress.pack(fill="x", **pad)

        self.status = tk.StringVar(value="⏳ First time Downloading it takes some time..")
        ttk.Label(root, textvariable=self.status, wraplength=520).pack(anchor="w", pady=(8, 0), **pad)

        ttk.Button(root, text="📂 Open Download folder", command=self.open_folder).pack(
            anchor="e", pady=(6, 0), **pad)

        threading.Thread(target=self.do_setup, daemon=True).start()

    # ---------- Setup ----------
    def do_setup(self):
        try:
            setup_dependencies()
            self.ui(lambda: (self.btn.config(state="normal"),
                             self.status.set("✅ Ready! Paste and press Download...")))
        except Exception as e:
            self.ui(lambda: self.status.set(
                f"❌ Setup not working...! Try again with internet connection ({e})"))

    def ui(self, fn):
        self.root.after(0, fn)

    # ---------- Button ----------
    def paste(self):
        try:
            self.url_var.set(self.root.clipboard_get().strip())
        except tk.TclError:
            pass

    def browse(self):
        d = filedialog.askdirectory(title="Choose where to save",
                                    initialdir=self.save_dir if os.path.isdir(self.save_dir) else None,
                                    parent=self.root)
        if d:
            d = os.path.normpath(d)
            self.save_dir = d
            self.dir_var.set(d)
            store_save_dir(d)

    def open_folder(self):
        try:
            os.makedirs(self.save_dir, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Folder problem", f"Cannot use this folder:\n{e}")
            return
        if os.name == "nt":
            os.startfile(self.save_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", self.save_dir])
        else:
            subprocess.Popen(["xdg-open", self.save_dir])

    def start(self):
        url = self.url_var.get().strip()
        if not url.startswith("http"):
            messagebox.showwarning("No link here", "Use a valid link (starting with http or https).")
            return
        mode, quality = OPTIONS[self.choice.get()]
        save_dir = self.save_dir
        try:
            os.makedirs(save_dir, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Folder problem",
                                 f"Cannot use this folder. Please choose another.\n{e}")
            return
        self.btn.config(state="disabled")
        self.progress["value"] = 0
        self.status.set("⏬ starting download...")
        threading.Thread(target=self.download, args=(url, mode, quality, save_dir), daemon=True).start()

    # ---------- Download ----------
    def hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                pct = d["downloaded_bytes"] * 100 / total
                speed = d.get("speed")
                sp = f" • {speed / 1024 / 1024:.1f} MB/s" if speed else ""
                self.ui(lambda: (self.progress.config(value=pct),
                                 self.status.set(f"⏬ downloading... {pct:.0f}%{sp}")))
        elif d["status"] == "finished":
            self.ui(lambda: (self.progress.config(value=100),
                             self.status.set("⚙️ processing (file created)...")))

    def download(self, url, mode, quality, save_dir):
        import yt_dlp

        outtmpl = os.path.join(save_dir, "%(title).150s.%(ext)s")
        common = {
            "outtmpl": outtmpl,
            "noplaylist": True,
            "ffmpeg_location": FFMPEG_PATH,
            "progress_hooks": [self.hook],
            "quiet": True,
            "no_warnings": True,
        }

        if mode == "mp3":
            opts = {
                **common,
                "format": "bestaudio/best",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
                     "preferredquality": quality},
                    {"key": "FFmpegMetadata"},
                ],
            }
        else:
            fmt = ("bestvideo+bestaudio/best" if quality == "best" else
                   f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]")
            opts = {**common, "format": fmt, "merge_output_format": "mp4"}

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.ui(lambda: (self.progress.config(value=100),
                             self.status.set(f"✅ Success! Saved in: {save_dir}")))
        except Exception as e:
            msg = str(e).splitlines()[-1][:200]
            self.ui(lambda: self.status.set(f"❌ Error: {msg}"))
        finally:
            self.ui(lambda: self.btn.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista" if os.name == "nt" else "clam")
    except tk.TclError:
        pass
    App(root)
    root.mainloop()
