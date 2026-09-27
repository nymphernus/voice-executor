#!/usr/bin/env python3
"""
Скрипт сборки exe через PyInstaller.

Использование:
    python scripts/build_exe.py
"""

import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent


def main():
    print("Сборка voice-executor.exe...")

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller не установлен. Установите: pip install pyinstaller")
        sys.exit(1)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "voice-executor.spec",
            "--clean",
        ],
        cwd=project_root,
    )

    if result.returncode == 0:
        print("Сборка завершена: dist/voice-executor.exe")
        print("\nВАЖНО: Для работы необходимо:")
        print("1. Скопировать config.example.toml рядом с exe (или переименовать в config.toml)")
        print("2. Скачать модель: python scripts/download_model.py")
        print("3. Папку models/ положить рядом с exe")
    else:
        print("Ошибка сборки")
        sys.exit(1)


if __name__ == "__main__":
    main()
