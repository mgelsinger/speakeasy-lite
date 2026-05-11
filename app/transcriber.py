import logging

from faster_whisper import WhisperModel

from config import MODEL_SIZE, MODELS_DIR

log = logging.getLogger(__name__)


class Transcriber:
    def __init__(self):
        self._model = None

    def load(self):
        log.info("Loading Whisper model: %s on CUDA", MODEL_SIZE)
        self._model = WhisperModel(
            MODEL_SIZE, device="cuda", compute_type="float16",
            download_root=MODELS_DIR,
        )
        log.info("Model loaded on GPU")

    def transcribe(self, wav_path):
        if not self._model:
            log.error("Model not loaded")
            return ""
        log.info("Transcription started")
        try:
            segments, _info = self._model.transcribe(wav_path, beam_size=5, language="en")
            text = " ".join(seg.text.strip() for seg in segments).strip()
            log.info("Transcription completed: %r", text)
            return text
        except Exception as e:
            log.error("Transcription failed: %s", e)
            return ""
