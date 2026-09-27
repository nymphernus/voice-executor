"""Управление моделью Vosk: проверка, скачивание."""

import logging
import time
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

        logger.info("Скачивание модели Vosk (~50 MB)...")
        print("Скачивание модели Vosk (~50 MB)...")

        # Создаём директорию models
        models_dir = self.model_path.parent
        models_dir.mkdir(parents=True, exist_ok=True)

        zip_path = models_dir / "model.zip"

        try:
            # Скачиваем с прогресс-баром
            self._download_with_progress(MODEL_URL, zip_path)

            print("\nРаспаковка модели...")
            logger.info("Распаковка модели...")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(models_dir)

            zip_path.unlink()  # Удаляем архив
            logger.info(f"Модель установлена: {self.model_path}")
            print(f"Модель установлена: {self.model_path}")
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

    def _download_with_progress(self, url: str, dest: Path) -> None:
        """
        Скачивает файл с прогресс-баром.

        Args:
            url: URL для скачивания.
            dest: Путь для сохранения.
        """
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0
                last_print = 0.0

                with open(dest, "wb") as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Обновляем прогресс каждые 100 мс
                        now = time.time()
                        if now - last_print > 0.1:
                            if total_size > 0:
                                percent = int(downloaded * 100) // total_size
                                mb = downloaded / 1024 / 1024
                                total_mb = total_size / 1024 / 1024
                                msg = f"\r  Прогресс: {percent}% ({mb:.1f}/{total_mb:.1f} MB)"
                                print(msg, end="")
                            else:
                                mb = downloaded / 1024 / 1024
                                print(f"\r  Скачано: {mb:.1f} MB", end="")
                            last_print = now

            print()  # Новая строка после прогресс-бара

        except Exception as e:
            raise RuntimeError(f"Ошибка скачивания: {e}") from e
