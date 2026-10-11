@echo off
setlocal
title Downloader Setup
cd /d "%~dp0"

echo ==========================================
echo    Video / MP3 Downloader - Setup
echo ==========================================
echo.

if not exist "%~dp0Downloader.pyw" (
  echo ERROR: Downloader.pyw must be in the same folder as this Setup.bat
  pause
  exit /b 1
)

set "PYW="
call :findpy
if defined PYW goto havepy

echo Python not found. Installing Python, please wait...
where winget >nul 2>nul
if errorlevel 1 (
  echo.
  echo winget was not found on this PC.
  echo Opening the Python download page. Install Python from there
  echo ^(tick "Add Python to PATH"^) and then run this Setup.bat again.
  start https://www.python.org/downloads/
  pause
  exit /b 1
)
winget install -e --id Python.Python.3.13 --scope user --silent --accept-package-agreements --accept-source-agreements
call :findpy
if not defined PYW (
  echo.
  echo Python was installed but could not be located yet.
  echo Please close this window and run Setup.bat one more time.
  pause
  exit /b 1
)

:havepy
set "PY=%PYW:pythonw.exe=python.exe%"
echo.
echo Using Python: %PY%
echo Installing required components ^(needs internet^)...
"%PY%" -m pip install -U --disable-pip-version-check yt-dlp imageio-ffmpeg
if errorlevel 1 (
  echo.
  echo Could not install components. Check your internet and run Setup.bat again.
  pause
  exit /b 1
)

set "APPDIR=%LocalAppData%\VideoDownloader"
if not exist "%APPDIR%" mkdir "%APPDIR%"
copy /y "%~dp0Downloader.pyw" "%APPDIR%\Downloader.pyw" >nul

set "VBS=%temp%\mkshortcut.vbs"
> "%VBS%" echo Set s = CreateObject("WScript.Shell")
>> "%VBS%" echo Set l = s.CreateShortcut(s.SpecialFolders("Desktop") ^& "\Video MP3 Downloader.lnk")
>> "%VBS%" echo l.TargetPath = "%PYW%"
>> "%VBS%" echo l.Arguments = Chr(34) ^& "%APPDIR%\Downloader.pyw" ^& Chr(34)
>> "%VBS%" echo l.WorkingDirectory = "%APPDIR%"
>> "%VBS%" echo l.Save
cscript //nologo "%VBS%"
del "%VBS%" >nul 2>nul

echo.
echo ==========================================
echo   DONE! A shortcut named
echo   "Video MP3 Downloader" is on your Desktop.
echo ==========================================
pause
exit /b 0

:findpy
for /f "delims=" %%I in ('where pythonw 2^>nul') do if not defined PYW set "PYW=%%I"
if defined PYW exit /b
for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do if exist "%%D\pythonw.exe" set "PYW=%%D\pythonw.exe"
if defined PYW exit /b
for /d %%D in ("%ProgramFiles%\Python3*") do if exist "%%D\pythonw.exe" set "PYW=%%D\pythonw.exe"
exit /b
