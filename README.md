# Speakeasy Lite

Local Windows dictation utility. Press a button, speak, stop — text appears where your cursor is.

No internet required after the model downloads on first run.

---

## Requirements

- Windows 11
- Python 3.11 or 3.12
- A microphone
- ~1.5 GB disk space for the Whisper model

---

## Setup

```powershell
.\scripts\setup.ps1
```

This creates a `.venv`, installs all dependencies, and downloads the Whisper Turbo model on first transcription.

---

## Run

```powershell
.\scripts\run.ps1
```

A tray icon appears in the system tray (bottom-right).

---

## Usage

| Trigger | Action |
|---|---|
| **Mouse Button 5** (forward thumb) | Toggle recording on/off |
| **Ctrl+Alt+D** | Toggle recording on/off |
| **Tray icon** → Toggle Recording | Toggle recording on/off |

**Flow:**
1. Click into the text field you want to type into (Discord, browser, etc.)
2. Trigger recording (button or hotkey)
3. Speak
4. Trigger again to stop
5. Text is pasted automatically

**Tray icon colors:**
- Green — idle
- Red — recording
- Orange — transcribing (Whisper running)

---

## Build (single .exe)

```powershell
.\scripts\build.ps1
```

Output: `dist\SpeakeasyLite.exe`

The first run will still download the Whisper model (~1.5 GB) unless you pre-cache it.

---

## Troubleshooting

**No tray icon appears**
- Check `speakeasy.log` in the project root for errors
- Make sure `.venv` is set up: run `.\scripts\setup.ps1`

**Recording doesn't start**
- Check that your microphone is the Windows default recording device
- `speakeasy.log` will show the error

**Text doesn't paste**
- Transcription runs after you stop recording — wait for the tray icon to turn green
- Make sure the target text field is still focused when you stop recording
- Some apps (games, elevated-privilege apps) block simulated input; try a browser instead

**Whisper model download fails**
- The model downloads from Hugging Face on first transcription
- If behind a proxy, set `HF_HUB_OFFLINE=1` after a successful download to prevent re-checks

**Slow transcription**
- Without a CUDA GPU, Whisper Turbo on CPU takes 5–15 seconds per clip
- Check `speakeasy.log` — it logs whether GPU or CPU was used at startup

**Ctrl+Alt+D conflicts with another app**
- Edit `app\hotkeys.py` line with `HotKey.parse` and change the combination

---

## Log file

`speakeasy.log` in the project root. Rotates automatically on each launch (appends).
