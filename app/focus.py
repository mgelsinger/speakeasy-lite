import ctypes
import logging
import threading
import time

log = logging.getLogger(__name__)

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

_EXCLUDED_CLASSES = frozenset({
    "Shell_TrayWnd",
    "Shell_SecondaryTrayWnd",
    "NotifyIconOverflowWindow",
    "TaskListThumbnailWnd",
})


class FocusTracker:
    def __init__(self):
        self._last_hwnd = None
        self._lock = threading.Lock()

    def start(self):
        threading.Thread(target=self._poll, daemon=True, name="focus-tracker").start()

    def restore(self):
        with self._lock:
            hwnd = self._last_hwnd
        if not hwnd:
            return
        try:
            self._force_foreground(hwnd)
            time.sleep(0.05)
        except Exception as e:
            log.debug("Focus restore failed: %s", e)

    def _force_foreground(self, hwnd):
        fg = _user32.GetForegroundWindow()
        fg_tid = _user32.GetWindowThreadProcessId(fg, None)
        our_tid = _kernel32.GetCurrentThreadId()
        tgt_tid = _user32.GetWindowThreadProcessId(hwnd, None)

        if fg_tid and fg_tid != our_tid:
            _user32.AttachThreadInput(fg_tid, our_tid, True)
        if tgt_tid and tgt_tid != our_tid and tgt_tid != fg_tid:
            _user32.AttachThreadInput(tgt_tid, our_tid, True)

        _user32.SetForegroundWindow(hwnd)
        _user32.BringWindowToTop(hwnd)

        if fg_tid and fg_tid != our_tid:
            _user32.AttachThreadInput(fg_tid, our_tid, False)
        if tgt_tid and tgt_tid != our_tid and tgt_tid != fg_tid:
            _user32.AttachThreadInput(tgt_tid, our_tid, False)

    def _poll(self):
        while True:
            try:
                hwnd = _user32.GetForegroundWindow()
                if hwnd:
                    buf = ctypes.create_unicode_buffer(256)
                    _user32.GetClassNameW(hwnd, buf, 256)
                    if buf.value not in _EXCLUDED_CLASSES:
                        with self._lock:
                            self._last_hwnd = hwnd
            except Exception:
                pass
            time.sleep(0.1)
