"""
Исполнитель команд — реестр действий.
"""

import inspect
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

    def execute(self, action_name: str, text: str = "") -> bool:
        """
        Выполняет действие по имени.

        Args:
            action_name: Имя действия.
            text: Распознанный текст (для команд, которым нужен контекст).

        Returns:
            True если действие найдено и выполнено.

        Raises:
            KeyError: Если действие не найдено.
        """
        if action_name not in self._actions:
            logger.error(f"Неизвестное действие: {action_name}")
            raise KeyError(f"Действие не найдено: {action_name}")

        action = self._actions[action_name]
        logger.info(f"Выполнение действия: {action_name}")

        # Проверяем, принимает ли функция аргумент text
        sig = inspect.signature(action)
        if len(sig.parameters) > 0:
            action(text)
        else:
            action()
        return True

    def has_action(self, name: str) -> bool:
        """Проверяет, зарегистрировано ли действие."""
        return name in self._actions
