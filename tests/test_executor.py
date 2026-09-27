"""
Тесты для модуля executor.
"""

from unittest.mock import MagicMock

import pytest

from voice_assistant.executor import CommandExecutor


class TestCommandExecutor:
    """Тесты CommandExecutor."""

    def test_register(self):
        executor = CommandExecutor()
        mock_action = MagicMock()
        executor.register("test", mock_action)
        assert executor.has_action("test")

    def test_execute(self):
        executor = CommandExecutor()
        mock_action = MagicMock()
        executor.register("test", mock_action)
        assert executor.execute("test") is True
        mock_action.assert_called_once()

    def test_execute_unknown(self):
        executor = CommandExecutor()
        with pytest.raises(KeyError):
            executor.execute("unknown")

    def test_has_action(self):
        executor = CommandExecutor()
        assert not executor.has_action("test")
        executor.register("test", MagicMock())
        assert executor.has_action("test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
