import logging

from pynput import keyboard, mouse

log = logging.getLogger(__name__)


class HotkeyListener:
    def __init__(self, on_toggle):
        self._on_toggle = on_toggle
        self._kb_listener = None
        self._mouse_listener = None
        self._hotkey = None
        self._mouse5_enabled = False

    def start(self):
        self._hotkey = keyboard.HotKey(
            keyboard.HotKey.parse("<ctrl>+<alt>+d"),
            self._on_toggle,
        )

        self._kb_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._mouse_listener = mouse.Listener(
            on_click=self._on_click,
        )
        self._kb_listener.start()
        self._mouse_listener.start()
        log.info("Hotkey listeners started (Ctrl+Alt+D, Mouse Button 5)")

    def stop(self):
        if self._kb_listener:
            self._kb_listener.stop()
        if self._mouse_listener:
            self._mouse_listener.stop()

    def set_mouse5_enabled(self, enabled: bool):
        self._mouse5_enabled = enabled
        log.info("Mouse Button 5 %s", "enabled" if enabled else "disabled")

    def _on_press(self, key):
        try:
            self._hotkey.press(self._kb_listener.canonical(key))
        except Exception:
            pass

    def _on_release(self, key):
        try:
            self._hotkey.release(self._kb_listener.canonical(key))
        except Exception:
            pass

    def _on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.x2 and self._mouse5_enabled:
            self._on_toggle()
