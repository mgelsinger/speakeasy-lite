import logging
import time

import pyperclip
from pynput.keyboard import Controller, Key

log = logging.getLogger(__name__)
_keyboard = Controller()


def insert_text(text):
    log.info("Insertion attempted")
    try:
        pyperclip.copy(text)
        time.sleep(0.05)  # let clipboard settle

        _keyboard.press(Key.ctrl)
        _keyboard.press("v")
        _keyboard.release("v")
        _keyboard.release(Key.ctrl)

        log.info("Insertion completed")
    except Exception as e:
        log.error("Insertion failed: %s", e)
