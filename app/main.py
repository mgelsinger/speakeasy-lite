import logging
import os
import sys
import threading

# Allow `import config` etc. from within the app/ directory
sys.path.insert(0, os.path.dirname(__file__))

# Add CUDA 12 bin to the DLL search path before ctranslate2 loads any CUDA libraries.
# This works regardless of how the process was launched (shell PATH may be stale
# if the CUDA installer ran in the same terminal session).
_CUDA_BIN = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin"
if os.path.isdir(_CUDA_BIN):
    os.add_dll_directory(_CUDA_BIN)
    os.environ["PATH"] = _CUDA_BIN + os.pathsep + os.environ.get("PATH", "")

from config import LOG_FILE, TEMP_DIR
from recorder import Recorder
from transcriber import Transcriber
from inserter import insert_text
from tray import TrayApp
from hotkeys import HotkeyListener
from focus import FocusTracker
import startup


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    setup_logging()
    log = logging.getLogger("main")
    log.info("Speakeasy Lite starting")

    transcriber = Transcriber()

    recorder = Recorder()

    focus_tracker = FocusTracker()
    focus_tracker.start()

    # State: idle | recording | processing
    # Toggle while processing is silently ignored.
    state = {"value": "idle"}
    state_lock = threading.Lock()

    ctx = {"tray": None}

    def finalize(wav_path):
        if wav_path:
            text = transcriber.transcribe(wav_path)
            if text:
                focus_tracker.restore()
                insert_text(text)
        with state_lock:
            state["value"] = "idle"
        if ctx["tray"]:
            ctx["tray"].set_state("idle")

    def on_toggle():
        with state_lock:
            current = state["value"]
            if current == "idle":
                state["value"] = "recording"
            elif current == "recording":
                state["value"] = "processing"
            else:
                return  # still processing — ignore

        if current == "idle":
            try:
                recorder.start()
            except Exception as e:
                log.error("Failed to start recording: %s", e)
                with state_lock:
                    state["value"] = "idle"
                return
            if ctx["tray"]:
                ctx["tray"].set_state("recording")

        elif current == "recording":
            wav_path = recorder.stop()
            if ctx["tray"]:
                ctx["tray"].set_state("processing")
            threading.Thread(target=finalize, args=(wav_path,), daemon=True).start()

    def on_exit():
        log.info("Exit requested")
        recorder.stop()
        hotkeys.stop()

    hotkeys = HotkeyListener(on_toggle=on_toggle)

    tray = TrayApp(
        on_toggle=on_toggle,
        on_exit=on_exit,
        on_mouse5_toggle=lambda: hotkeys.set_mouse5_enabled(not hotkeys._mouse5_enabled),
        is_mouse5_enabled=lambda: hotkeys._mouse5_enabled,
        on_startup_toggle=lambda: startup.set_enabled(not startup.is_enabled()),
        is_startup_enabled=startup.is_enabled,
    )
    ctx["tray"] = tray

    hotkeys.start()

    def _load_model():
        import time as _time
        _time.sleep(0.5)  # let tray icon initialize
        with state_lock:
            state["value"] = "processing"
        if ctx["tray"]:
            ctx["tray"].set_state("processing")
        try:
            transcriber.load()
            with state_lock:
                state["value"] = "idle"
            if ctx["tray"]:
                ctx["tray"].set_state("idle")
                ctx["tray"].notify("Ready to dictate.")
        except Exception as e:
            log.error("Model load failed: %s", e)
            if ctx["tray"]:
                ctx["tray"].notify("Error: model failed to load. See speakeasy.log.")

    threading.Thread(target=_load_model, daemon=True).start()

    tray.run()  # blocks; returns when user clicks Exit
    log.info("Speakeasy Lite stopped")


if __name__ == "__main__":
    main()
