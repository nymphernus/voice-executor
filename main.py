"""
Тонкая обёртка для запуска голосового ассистента.

Запуск:
    python main.py
"""

import sys
from pathlib import Path

# Добавляем src в sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_assistant.app import main

if __name__ == "__main__":
    main()
