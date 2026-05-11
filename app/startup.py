import logging
import os
import sys
import winreg

from config import BASE_DIR

log = logging.getLogger(__name__)

_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
_APP_NAME = "SpeakeasyLite"
_LAUNCH_VBS = os.path.join(BASE_DIR, "launch.vbs")


def is_enabled() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, _APP_NAME)
        winreg.CloseKey(key)
        return True
    except OSError:
        return False


def set_enabled(enabled: bool):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_PATH, 0, winreg.KEY_SET_VALUE)
        if enabled:
            if getattr(sys, "frozen", False):
                value = f'"{sys.executable}"'
            else:
                value = f'wscript.exe "{_LAUNCH_VBS}"'
            winreg.SetValueEx(key, _APP_NAME, 0, winreg.REG_SZ, value)
            log.info("Added to Windows startup: %s", value)
        else:
            try:
                winreg.DeleteValue(key, _APP_NAME)
                log.info("Removed from Windows startup")
            except OSError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        log.error("Failed to update startup registry: %s", e)
