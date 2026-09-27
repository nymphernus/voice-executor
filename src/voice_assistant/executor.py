"""
Исполнитель команд — реестр действий.
"""

import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Реестр и исполнитель команд."""

    def __init__(self):
        self._actions: dict[str, Callable] = {}

    def register(self, name: str, action: Callable) -> None:
        """
        Регистрирует действие.

        Args:
            name: Имя действия.
            action: Функция-обработчик.
        """
        self._actions[name] = action
        logger.debug(f"Зарегистрировано действие: {name}")

    def execute(self, action_name: str) -> bool:
        """
        Выполняет действие по имени.

        Args:
            action_name: Имя действия.

        Returns:
            True если действие найдено и выполнено.

        Raises:
            KeyError: Если действие не найдено.
        """
        if action_name not in self._actions:
            logger.error(f"Неизвестное действие: {action_name}")
            raise KeyError(f"Действие не найдено: {action_name}")

        logger.info(f"Выполнение действия: {action_name}")
        self._actions[action_name]()
        return True

    def has_action(self, name: str) -> bool:
        """Проверяет, зарегистрировано ли действие."""
        return name in self._actions
