"""Команды Discord."""

import ctypes
import logging

logger = logging.getLogger(__name__)

VK_MENU = 0x12  # Alt
VK_F2 = 0x71  # F2


def do_alt_f2() -> None:
    """
    Нажимает Alt+F2 (переключение микрофона в Discord).
    """
    logger.info("Переключение микрофона в Discord (Alt+F2)")
    print("Переключаю микрофон в Discord (Alt+F2)...")
    try:
        user32 = ctypes.windll.user32
        # Нажимаем Alt
        user32.keybd_event(VK_MENU, 0, 0, 0)
        # Нажимаем F2
        user32.keybd_event(VK_F2, 0, 0, 0)
        # Отпускаем F2
        user32.keybd_event(VK_F2, 0, 2, 0)
        # Отпускаем Alt
        user32.keybd_event(VK_MENU, 0, 2, 0)
    except Exception as e:
        logger.error(f"Ошибка нажатия Alt+F2: {e}")
