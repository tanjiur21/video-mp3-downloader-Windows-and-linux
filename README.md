# Video / MP3 Downloader

A simple desktop tool to download videos or MP3 songs from YouTube, Instagram and many other sites. Paste a link, choose a quality, click **Download**. No ads, no complicated commands.

Built with Python, [yt-dlp](https://github.com/yt-dlp/yt-dlp) and a small Tkinter window.
**Download** ZIp.rar and extract there have everything... :) 

**Program by Tanjiur Rahman Twha**

## Features

- Paste a link and download with one click
- MP3 (320 kbps or 192 kbps) or video (Max, 1080p, 720p, 480p)
- Choose the folder where files are saved (remembered next time)
- Progress bar with download speed
- Updates yt-dlp automatically once a day, so downloads keep working
- No separate ffmpeg install needed (it is set up automatically)
- One-click setup for Windows

## Files

| File | Purpose |
|------|---------|
| `Downloader.pyw` | The program |
| `Setup.bat` | One-click setup for Windows (installs Python and everything needed, creates a Desktop shortcut) |

## Windows setup (once per PC)

1. Download this repository (green **Code** button, then **Download ZIP**) and extract it.
2. Make sure `Setup.bat` and `Downloader.pyw` are in the same folder.
3. Double-click `Setup.bat`.
   If Windows shows "Windows protected your PC", click **More info**, then **Run anyway**.
4. Wait 2-5 minutes (internet needed). A shortcut named **Video MP3 Downloader** appears on your Desktop.

## Linux setup

```bash
sudo apt install python3 python3-tk python3-venv
python3 -m venv ~/videodl
~/videodl/bin/pip install yt-dlp imageio-ffmpeg
~/videodl/bin/python Downloader.pyw
```

(Fedora: `sudo dnf install python3 python3-tkinter` / Arch: `sudo pacman -S python tk`)

## How to use

1. Open **Video MP3 Downloader** and wait for the message "Ready!"
2. Copy a video link, click **Paste**
3. Choose MP3 or a video quality
4. Choose the save folder with **Browse** (optional)
5. Click **Download**
6. Click **Open Download folder** to find your file

Default save folder: `Downloads/MyDownloads`

## Troubleshooting

- **Setup not working**: check your internet connection and open the program again.
- **Download error**: make sure the link starts with `http`, the video is public, then reopen the program so it can update itself and try again.
- **Setup.bat cannot find Python after install**: close the window and run `Setup.bat` once more.
- **No `winget` on Windows**: install Python from [python.org](https://www.python.org/downloads/) (tick "Add Python to PATH"), then run `Setup.bat` again.

## Disclaimer

This tool is for **personal use only**. Downloading content may violate the terms of the website or the rights of the content owner. You are responsible for how you use it. Respect copyright and do not share or sell downloaded content. Private or login-only videos and playlists are not supported.

This project is not affiliated with YouTube, Instagram or any other website.

## License

MIT License. See [LICENSE](LICENSE).
