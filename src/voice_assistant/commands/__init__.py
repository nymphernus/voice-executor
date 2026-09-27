"""
Реестр команд голосового ассистента.
"""

import logging

from voice_assistant.commands import apps, browser, discord, system
from voice_assistant.executor import CommandExecutor

logger = logging.getLogger(__name__)


def register_commands(executor: CommandExecutor) -> None:
    """
    Регистрирует все команды в исполнителе.

    Args:
        executor: Исполнитель команд.
    """
    # Системные команды
    executor.register("exit", system.do_exit)
    executor.register("f5", system.do_f5)
    executor.register("taskmanager", system.do_taskmanager)
    executor.register("terminal", system.do_terminal)
    executor.register("screenshot", system.do_screenshot)
    executor.register("timer", system.do_timer)

    # Браузер
    executor.register("youtube", browser.do_youtube)

    # Приложения
    executor.register("dota", apps.do_dota)
    executor.register("phpstorm", apps.do_phpstorm)

    # Discord
    executor.register("alt+f2", discord.do_alt_f2)

    logger.info(f"Зарегистрировано команд: {len(executor._actions)}")
