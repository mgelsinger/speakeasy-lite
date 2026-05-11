import logging

from PIL import Image, ImageDraw
import pystray

log = logging.getLogger(__name__)

_STATE_CFG = {
    "idle":       {"color": (50, 180, 50),  "title": "Speakeasy Lite — Idle"},
    "recording":  {"color": (220, 50, 50),  "title": "Speakeasy Lite — Recording..."},
    "processing": {"color": (220, 140, 50), "title": "Speakeasy Lite — Processing..."},
}


def _make_icon(color):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=color)
    return img


class TrayApp:
    def __init__(self, on_toggle, on_exit, on_mouse5_toggle, is_mouse5_enabled,
                 on_startup_toggle, is_startup_enabled):
        self._on_toggle = on_toggle
        self._on_exit = on_exit
        self._on_mouse5_toggle = on_mouse5_toggle
        self._is_mouse5_enabled = is_mouse5_enabled
        self._on_startup_toggle = on_startup_toggle
        self._is_startup_enabled = is_startup_enabled
        self._icon = None

    def set_state(self, state):
        if not self._icon:
            return
        cfg = _STATE_CFG.get(state, _STATE_CFG["idle"])
        self._icon.icon = _make_icon(cfg["color"])
        self._icon.title = cfg["title"]

    def notify(self, message):
        try:
            if self._icon:
                self._icon.notify(message, "Speakeasy Lite")
        except Exception:
            pass

    def _handle_exit(self):
        self._on_exit()
        if self._icon:
            self._icon.stop()

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("Toggle Recording", lambda: self._on_toggle(), default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Mouse Button 5",
                lambda: self._on_mouse5_toggle(),
                checked=lambda item: self._is_mouse5_enabled(),
            ),
            pystray.MenuItem(
                "Run at startup",
                lambda: self._on_startup_toggle(),
                checked=lambda item: self._is_startup_enabled(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._handle_exit),
        )
        self._icon = pystray.Icon(
            "speakeasy-lite",
            icon=_make_icon(_STATE_CFG["idle"]["color"]),
            title=_STATE_CFG["idle"]["title"],
            menu=menu,
        )
        log.info("Tray icon running")
        self._icon.run()  # blocks until exit
