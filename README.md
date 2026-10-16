# Video / MP3 Downloader

A simple desktop app to download videos or MP3 songs from YouTube, Instagram and many other sites.
Paste a link, pick a format, and let it run. No ads, no commands... 

Built with Python, [yt-dlp](https://github.com/yt-dlp/yt-dlp) and Tkinter.
**By tanjiur21**

## Features

- Paste a link and see the video title before downloading
- **MP3** (320 / 192 / 128 kbps) or **Video** (Max, 1080p, 720p, 480p, 360p)
- **Download queue**: add many links, they download one by one
- Download a **whole playlist** into its own folder
- **Auto-organize**: songs go to `Music`, videos go to `Videos`
- Choose your save folder (remembered next time)
- Cancel a download, or clear the finished ones
- Auto-updates yt-dlp once a day, plus an **Update** button
- No separate ffmpeg install needed

## Files

| File |
`Downloader.pyw`
`Setup.bat` 

| What it does |

| `Downloader.pyw` | The app |
| `Setup.bat` | One-click setup for Windows (installs everything and adds a Desktop shortcut) |

## Install on Windows

1. Click the green **Code** button, then **Download ZIP**, and extract it.
2. Keep `Setup.bat` and `Downloader.pyw` in the same folder.
3. Double-click **`Setup.bat`** and wait 2-5 minutes (internet needed).
   If Windows says "Windows protected your PC", click **More info**, then **Run anyway**.
4. Open **Video MP3 Downloader** from your Desktop.

## Install on Linux

```bash
sudo apt install python3 python3-tk python3-venv
python3 -m venv ~/videodl
~/videodl/bin/pip install yt-dlp imageio-ffmpeg
~/videodl/bin/python Downloader.pyw
```

## How to use

1. Copy a video link. It appears in the box automatically (or click **Paste**).
2. Choose **MP3** or **Video** and the quality.
3. Choose where to save with **Browse** (optional).
4. Click **Add to downloads**. Add more links any time.
5. Click **Open folder** to find your files.

Default folder: `Downloads/MyDownloads`

## Settings

Click **Settings** to:

- **Browser login**: fixes the YouTube message *"Sign in to confirm you're not a bot"*. Otherwise it make some problem..
  Choose the browser where you are logged in to YouTube (Firefox works best).
- **Auto-organize**: turn the Music / Videos folders on or off.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Sign in to confirm you're not a bot" | Open **Settings** and choose your browser, then add the link again |
| A download shows **Failed** | Double-click it to see the reason |
| Downloads suddenly stop working | Click **Update yt-dlp**, then restart the app |
| Setup failed | Check your internet connection and open the app again |
| Setup.bat can't find Python | Close it and run `Setup.bat` once more |
| No `winget` on Windows | Install Python from [python.org](https://www.python.org/downloads/) (tick "Add Python to PATH"), then run `Setup.bat` again |

## Disclaimer

For **personal use only**. Downloading content may break a website's terms or the owner's rights.
You are responsible for how you use this tool. Respect copyright and do not share or sell downloaded content.
Private or login-only videos may not work.
This project is not affiliated with YouTube, Instagram or any other website.

## License

MIT License. See [LICENSE](LICENSE).
