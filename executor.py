"""
Исполнитель команд.
Связывает распознанный текст с действиями.
"""

from config import TRIGGERS, MAX_COMMAND_WORDS
from commands import ACTIONS
from recognizer import normalize_text


class CommandExecutor:
    """Исполняет команды на основе распознанного текста."""

    def __init__(self, triggers=None, actions=None):
        """
        Args:
            triggers: Словарь триггеров {слово: действие}.
            actions: Словарь действий {имя: функция}.
        """
        self.triggers = triggers or TRIGGERS
        self.actions = actions or ACTIONS

    def execute(self, text: str) -> bool:
        """
        Проверяет текст на наличие команд и выполняет их.

        Args:
            text: Распознанный текст.

        Returns:
            True если команда найдена и выполнена.
        """
        text_lower = normalize_text(text)
        words = text_lower.split()

        # Защита: если слов больше MAX_COMMAND_WORDS — пропускаем
        if len(words) > MAX_COMMAND_WORDS:
            return False

        # Точное совпадение
        if text_lower in self.triggers:
            return self._do_action(self.triggers[text_lower])

        # Поиск триггера
        for trigger, action in self.triggers.items():
            if trigger in text_lower:
                return self._do_action(action)

        return False

    def _do_action(self, action: str) -> bool:
        """Выполняет действие по имени."""
        if action in self.actions:
            self.actions[action]()
            return True
        return False
