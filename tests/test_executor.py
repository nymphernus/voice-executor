"""
Тесты для модуля executor.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from executor import CommandExecutor


class TestCommandExecutor:
    """Тесты CommandExecutor."""

    def test_execute_exit(self):
        mock_exit = MagicMock()
        executor = CommandExecutor(actions={"exit": mock_exit})
        assert executor.execute("стоп") is True
        mock_exit.assert_called_once()

    def test_execute_alt_f2(self):
        mock_alt_f2 = MagicMock()
        executor = CommandExecutor(actions={"alt+f2": mock_alt_f2})
        assert executor.execute("микрофон") is True
        mock_alt_f2.assert_called_once()

    def test_execute_dota(self):
        mock_dota = MagicMock()
        executor = CommandExecutor(actions={"steam://rungameid/570": mock_dota})
        assert executor.execute("дота") is True
        mock_dota.assert_called_once()

    def test_execute_phpstorm(self):
        mock_phpstorm = MagicMock()
        executor = CommandExecutor(actions={"phpstorm": mock_phpstorm})
        assert executor.execute("шторм") is True
        mock_phpstorm.assert_called_once()

    def test_execute_youtube(self):
        mock_youtube = MagicMock()
        executor = CommandExecutor(actions={"https://www.youtube.com": mock_youtube})
        assert executor.execute("ютуб") is True
        mock_youtube.assert_called_once()

    def test_execute_f5(self):
        mock_f5 = MagicMock()
        executor = CommandExecutor(actions={"f5": mock_f5})
        assert executor.execute("обновить") is True
        mock_f5.assert_called_once()

    def test_execute_refresh_short(self):
        mock_f5 = MagicMock()
        executor = CommandExecutor(actions={"f5": mock_f5})
        assert executor.execute("обнови") is True
        mock_f5.assert_called_once()

    def test_sentence_protection_exit(self):
        mock_exit = MagicMock()
        executor = CommandExecutor(actions={"exit": mock_exit})
        assert executor.execute("стоп что ты делаешь") is False
        mock_exit.assert_not_called()

    def test_sentence_protection_microphone(self):
        mock_alt_f2 = MagicMock()
        executor = CommandExecutor(actions={"alt+f2": mock_alt_f2})
        assert executor.execute("включи микрофон пожалуйста") is False
        mock_alt_f2.assert_not_called()

    def test_sentence_protection_youtube(self):
        mock_youtube = MagicMock()
        executor = CommandExecutor(actions={"https://www.youtube.com": mock_youtube})
        assert executor.execute("открой ютуб с музыкой") is False
        mock_youtube.assert_not_called()

    def test_sentence_protection_refresh(self):
        mock_f5 = MagicMock()
        executor = CommandExecutor(actions={"f5": mock_f5})
        assert executor.execute("обнови страницу сейчас") is False
        mock_f5.assert_not_called()

    def test_no_match(self):
        executor = CommandExecutor()
        assert executor.execute("какая погода") is False

    def test_empty(self):
        executor = CommandExecutor()
        assert executor.execute("") is False

    def test_case_insensitive(self):
        mock_phpstorm = MagicMock()
        executor = CommandExecutor(actions={"phpstorm": mock_phpstorm})
        assert executor.execute("ШтОрМ") is True
        mock_phpstorm.assert_called_once()


class TestCustomExecutor:
    """Тесты с пользовательскими триггерами."""

    def test_custom_trigger(self):
        custom_triggers = {"тест": "test_action"}
        custom_actions = {"test_action": MagicMock()}

        executor = CommandExecutor(triggers=custom_triggers, actions=custom_actions)
        assert executor.execute("тест") is True
        custom_actions["test_action"].assert_called_once()

    def test_custom_action_not_found(self):
        custom_triggers = {"тест": "unknown_action"}
        custom_actions = {}

        executor = CommandExecutor(triggers=custom_triggers, actions=custom_actions)
        assert executor.execute("тест") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
