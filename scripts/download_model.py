#!/usr/bin/env python3
"""
Скрипт скачивания модели Vosk.

Использование:
    python scripts/download_model.py [--model small|big] [--force]
"""

import argparse
import sys
from pathlib import Path

# Добавляем src в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_assistant.model_manager import ModelManager


def main():
    parser = argparse.ArgumentParser(description="Скачивание модели Vosk")
    parser.add_argument(
        "--model",
        choices=["small", "big"],
        default="small",
        help="Размер модели (small ~50MB, big ~1.5GB)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Перескачать, даже если модель существует",
    )
    args = parser.parse_args()

    if args.model == "small":
        model_path = "models/vosk-model-small-ru-0.22"
    else:
        model_path = "models/vosk-model-ru-0.42"

    manager = ModelManager(model_path)

    if manager.exists() and not args.force:
        print(f"Модель уже существует: {model_path}")
        return

    try:
        path = manager.download(force=args.force)
        print(f"Модель скачана: {path}")
    except RuntimeError as e:
        print(f"Ошибка: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте подключение к интернету")
        print("2. Скачайте вручную: https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip")
        print("3. Распакуйте в папку models/")
        sys.exit(1)


if __name__ == "__main__":
    main()
