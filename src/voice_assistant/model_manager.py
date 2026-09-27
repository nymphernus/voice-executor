"""Управление моделью Vosk: проверка, скачивание."""

import logging
import os
import urllib.request
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
MODEL_DIR_NAME = "vosk-model-small-ru-0.22"


class ModelManager:
    """Управляет моделью Vosk."""

    def __init__(self, model_path: str):
        """
        Args:
            model_path: Путь к директории модели.
        """
        self.model_path = Path(model_path)

    def exists(self) -> bool:
        """Проверяет, существует ли модель."""
        return self.model_path.exists()

    def download(self, force: bool = False) -> Path:
        """
        Скачивает модель Vosk.

        Args:
            force: Перескачать, даже если модель существует.

        Returns:
            Путь к директории модели.

        Raises:
            RuntimeError: Если скачивание не удалось.
        """
        if self.exists() and not force:
            logger.info(f"Модель уже существует: {self.model_path}")
            return self.model_path

        logger.info(f"Скачивание модели Vosk (~50 MB)...")

        # Создаём директорию models
        models_dir = self.model_path.parent
        models_dir.mkdir(parents=True, exist_ok=True)

        zip_path = models_dir / "model.zip"

        try:
            urllib.request.urlretrieve(MODEL_URL, zip_path)
            logger.info("Распаковка модели...")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(models_dir)

            zip_path.unlink()  # Удаляем архив
            logger.info(f"Модель установлена: {self.model_path}")
            return self.model_path

        except Exception as e:
            if zip_path.exists():
                zip_path.unlink()
            raise RuntimeError(f"Не удалось скачать модель: {e}") from e

    def ensure_model(self) -> Path:
        """
        Гарантирует наличие модели, скачивает при необходимости.

        Returns:
            Путь к директории модели.
        """
        if not self.exists():
            return self.download()
        return self.model_path
