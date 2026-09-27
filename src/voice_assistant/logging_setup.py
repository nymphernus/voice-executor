"""Настройка логирования."""

import logging
import logging.handlers
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "assistant.log",
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    """
    Настраивает логирование: консоль + файл с ротацией.

    Args:
        log_dir: Директория для логов.
        log_file: Имя файла лога.
        level: Уровень логирования.
        max_bytes: Максимальный размер файла лога (5 MB).
        backup_count: Количество архивных файлов.

    Returns:
        Настроенный логгер.
    """
    logger = logging.getLogger("voice_assistant")
    logger.setLevel(level)

    # Формат
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консоль
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # Файл с ротацией
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
