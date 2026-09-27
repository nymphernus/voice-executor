"""Системные команды."""

import ctypes
import logging
import os
import platform
import subprocess
import sys
import webbrowser

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


def do_taskmanager() -> None:
    """Открывает диспетчер задач."""
    logger.info("Открытие диспетчера задач")
    print("Открываю диспетчер задач...")
    try:
        subprocess.Popen(["taskmgr.exe"])
    except FileNotFoundError:
        logger.error("taskmgr.exe не найден")
        print("Ошибка: диспетчер задач не найден")
    except Exception as e:
        logger.error(f"Ошибка запуска диспетчера задач: {e}")


def do_terminal() -> None:
    """Открывает терминал."""
    logger.info("Открытие терминала")
    print("Открываю терминал...")
    system = platform.system()

    try:
        if system == "Windows":
            # Пробуем Windows Terminal, потом cmd
            try:
                subprocess.Popen(["wt.exe"])
            except FileNotFoundError:
                subprocess.Popen(["cmd.exe"])
        elif system == "Linux":
            # Пробуем распространённые терминалы Linux
            for term in ["gnome-terminal", "konsole", "xterm", "terminator"]:
                try:
                    subprocess.Popen([term])
                    break
                except FileNotFoundError:
                    continue
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Terminal"])
    except Exception as e:
        logger.error(f"Ошибка запуска терминала: {e}")


def do_screenshot() -> None:
    """Делает скриншот рабочего стола."""
    logger.info("Создание скриншота")
    print("Делаю скриншот...")

    try:
        from PIL import ImageGrab

        screenshot = ImageGrab.grab()

        # Сохраняем в рабочий стол или в текущую директорию
        save_path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.png")
        screenshot.save(save_path)
        logger.info(f"Скриншот сохранён: {save_path}")
        print(f"Скриншот сохранён: {save_path}")

    except ImportError:
        logger.error("Pillow не установлен")
        print("Ошибка: Pillow не установлен. Установите: pip install Pillow")
    except Exception as e:
        logger.error(f"Ошибка создания скриншота: {e}")


def do_timer() -> None:
    """Открывает таймер в браузере."""
    logger.info("Открытие таймера")
    print("Открываю таймер...")
    webbrowser.open("https://www.google.com/search?q=timer")
