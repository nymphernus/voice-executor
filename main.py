"""
Голосовой ассистент — точка входа.

Запуск:
    python main.py
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODEL_PATH, TRIGGERS
from recognizer import listen_continuous
from executor import CommandExecutor


def download_model(model_dir: str = "models") -> str:
    """Скачивает модель Vosk, если не найдена."""
    from pathlib import Path

    model_path = Path(model_dir) / "vosk-model-small-ru-0.22"

    if model_path.exists():
        print(f"Модель найдена: {model_path}")
        return str(model_path)

    print(f"Модель не найдена: {model_path}")
    print("Скачиваю модель (~50 MB)...")

    import urllib.request
    import zipfile

    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
    os.makedirs(model_dir, exist_ok=True)
    zip_path = os.path.join(model_dir, "model.zip")

    try:
        urllib.request.urlretrieve(model_url, zip_path)
        print("Распаковываю...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(model_dir)
        os.remove(zip_path)
        print(f"Модель установлена: {model_path}")
        return str(model_path)
    except Exception as e:
        print(f"Ошибка: {e}")
        print(f"Скачайте вручную: {model_url}")
        sys.exit(1)


def main():
    # Проверяем/скачиваем модель
    model_path = MODEL_PATH
    if not os.path.exists(model_path):
        model_path = download_model()

    # Создаём исполнитель команд
    executor = CommandExecutor()

    # Запускаем непрерывное прослушивание
    print("=" * 50)
    print("  Голосовой ассистент запущен")
    print("=" * 50)
    print(f"Модель: {model_path}")
    print(f"Команды: {', '.join(TRIGGERS.keys())}")
    print(f"Макс. слов в команде: 2")
    print("Ctrl+C — остановка.")
    print()

    def on_recognized(text):
        print(f"Распознано: {text}")
        executor.execute(text)
        print()

    listen_continuous(model_path, on_recognized=on_recognized)


if __name__ == "__main__":
    main()
