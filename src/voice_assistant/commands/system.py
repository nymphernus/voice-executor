"""Системные команды."""

import ctypes
import logging
import platform
import re
import subprocess
import sys
import webbrowser

logger = logging.getLogger(__name__)

VK_F5 = 0x74
VK_LWIN = 0x5B  # Left Windows key
VK_S = 0x53  # S key


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
        # Запускаем через shell для обхода требования прав администратора
        subprocess.Popen("taskmgr.exe", shell=True)
    except Exception as e:
        logger.error(f"Ошибка запуска диспетчера задач: {e}")


def do_terminal() -> None:
    """Открывает терминал."""
    logger.info("Открытие терминала")
    print("Открываю терминал...")
    system = platform.system()

    try:
        if system == "Windows":
            try:
                subprocess.Popen(["wt.exe"])
            except FileNotFoundError:
                subprocess.Popen(["cmd.exe"])
        elif system == "Linux":
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
    """Делает скриншот через Shift+Win+S (встроенная функция Windows)."""
    logger.info("Создание скриншота через Shift+Win+S")
    print("Делаю скриншот...")

    if platform.system() != "Windows":
        logger.error("Скриншот через Shift+Win+S поддерживается только на Windows")
        print("Ошибка: скриншот поддерживается только на Windows")
        return

    try:
        user32 = ctypes.windll.user32

        # Отпускаем клавиши
        user32.keybd_event(VK_LWIN, 0, 0x0002, 0)
        user32.keybd_event(VK_S, 0, 0x0002, 0)

        # Нажимаем Win+Shift+S
        user32.keybd_event(VK_LWIN, 0, 0, 0)
        user32.keybd_event(0x10, 0, 0, 0)  # Shift
        user32.keybd_event(VK_S, 0, 0, 0)

        # Отпускаем в обратном порядке
        user32.keybd_event(VK_S, 0, 0x0002, 0)
        user32.keybd_event(0x10, 0, 0x0002, 0)
        user32.keybd_event(VK_LWIN, 0, 0x0002, 0)

        logger.info("Скриншот активирован")
    except Exception as e:
        logger.error(f"Ошибка создания скриншота: {e}")


def do_timer(text: str = "") -> None:
    """
    Открывает таймер в браузере.

    Args:
        text: Распознанный текст (может содержать число минут).
    """
    logger.info("Открытие таймера")
    print("Открываю таймер...")

    # Парсим число из текста
    minutes = _extract_minutes(text)

    if minutes:
        url = f"https://www.google.com/search?q={minutes}+minute+timer"
        logger.info(f"Таймер на {minutes} минут")
        print(f"Таймер на {minutes} минут...")
    else:
        url = "https://www.google.com/search?q=timer"
        print("Открываю таймер...")

    webbrowser.open(url)


def _extract_minutes(text: str) -> int | None:
    """
    Извлекает количество минут из текста.

    Args:
        text: Распознанный текст.

    Returns:
        Количество минут или None.
    """
    # Числа словами (русские)
    number_words = {
        "одну": 1,
        "один": 1,
        "одна": 1,
        "две": 2,
        "два": 2,
        "двух": 2,
        "три": 3,
        "трёх": 3,
        "трех": 3,
        "четыре": 4,
        "четырёх": 4,
        "четырех": 4,
        "пять": 5,
        "пяти": 5,
        "шесть": 6,
        "шести": 6,
        "семь": 7,
        "семи": 7,
        "восемь": 8,
        "восьми": 8,
        "девять": 9,
        "девяти": 9,
        "десять": 10,
        "десяти": 10,
        "пятнадцать": 15,
        "пятнадцати": 15,
        "двадцать": 20,
        "двадцати": 20,
        "тридцать": 30,
        "тридцати": 30,
        "сорок": 40,
        "сорока": 40,
        "шестьдесят": 60,
        "шестидесяти": 60,
    }

    text_lower = text.lower()

    # Ищем число словами
    for word, num in number_words.items():
        if word in text_lower:
            return num

    # Ищем цифры
    match = re.search(r"(\d+)", text)
    if match:
        return int(match.group(1))

    return None
