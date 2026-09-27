"""Системные команды."""

import ctypes
import logging
import sys

logger = logging.getLogger(__name__)

VK_F5 = 0x74


def do_exit() -> None:
    """Завершение работы."""
    logger.info("Завершение работы...")
    print("Завершение работы...")
    sys.exit(0)


def do_f5() -> None:
    """Нажимает F5 (обновление страницы)."""
    logger.info("Обновление страницы (F5)")
    print("Обновляю страницу (F5)...")
    try:
        user32 = ctypes.windll.user32
        user32.keybd_event(VK_F5, 0, 0, 0)
        user32.keybd_event(VK_F5, 0, 2, 0)
    except Exception as e:
        logger.error(f"Ошибка нажатия F5: {e}")
