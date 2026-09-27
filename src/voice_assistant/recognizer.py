"""Распознавание речи через Vosk."""

import json
import logging
from collections.abc import Callable

from vosk import KaldiRecognizer, Model, SetLogLevel

from voice_assistant.audio import create_audio_stream
from voice_assistant.config import RecognitionConfig

SetLogLevel(-1)
logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """Распознаватель речи на базе Vosk."""

    def __init__(self, config: RecognitionConfig):
        """
        Args:
            config: Настройки распознавания.
        """
        self.config = config
        self._model = None
        self._recognizer = None
        self._audio = None
        self._stream = None

    def load_model(self) -> None:
        """Загружает модель Vosk."""
        logger.info(f"Загрузка модели: {self.config.model_path}")
        self._model = Model(self.config.model_path)
        recognizer = KaldiRecognizer(self._model, self.config.sample_rate)
        recognizer.SetWords(True)
        recognizer.SetPartialWords(True)
        self._recognizer = recognizer
        logger.info("Модель загружена")

    def start(self) -> None:
        """Запускает аудиопоток."""
        self._audio, self._stream = create_audio_stream(
            sample_rate=self.config.sample_rate,
            chunk_size=self.config.chunk_size,
            device=self.config.device,
        )

    def stop(self) -> None:
        """Останавливает аудиопоток и освобождает ресурсы."""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._audio:
            self._audio.terminate()
            self._audio = None
        logger.info("Аудиопоток остановлен")

    def listen(
        self,
        on_final: Callable[[str], None],
        on_partial: Callable[[str], None] | None = None,
    ) -> None:
        """
        Непрерывно слушает микрофон и распознаёт речь.

        Args:
            on_final: Колбэк для финального результата.
            on_partial: Колбэк для промежуточного результата (опционально).
        """
        if not self._recognizer:
            raise RuntimeError("Модель не загружена. Вызовите load_model()")

        logger.info("Начало прослушивания...")
        try:
            while True:
                data = self._stream.read(self.config.chunk_size, exception_on_overflow=False)

                if self._recognizer.AcceptWaveform(data):
                    result = json.loads(self._recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        logger.debug(f"Финальный результат: {text}")
                        on_final(text)
                elif on_partial:
                    result = json.loads(self._recognizer.PartialResult())
                    text = result.get("partial", "").strip()
                    if text:
                        on_partial(text)
        except KeyboardInterrupt:
            logger.info("Остановка по KeyboardInterrupt")
        finally:
            self.stop()
