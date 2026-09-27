"""Команды браузера."""

import logging
import webbrowser

logger = logging.getLogger(__name__)


def do_youtube() -> None:
    """Открывает YouTube в браузере."""
    logger.info("Открытие YouTube")
    print("Открываю YouTube...")
    webbrowser.open("https://www.youtube.com")
