"""
Тесты для реестра команд.
"""

import pytest

from voice_assistant.commands import register_commands
from voice_assistant.executor import CommandExecutor


class TestRegisterCommands:
    """Тесты регистрации команд."""

    def test_register_all(self):
        executor = CommandExecutor()
        register_commands(executor)

        assert executor.has_action("exit")
        assert executor.has_action("alt+f2")
        assert executor.has_action("dota")
        assert executor.has_action("phpstorm")
        assert executor.has_action("youtube")
        assert executor.has_action("f5")

    def test_register_count(self):
        executor = CommandExecutor()
        register_commands(executor)

        # 6 команд: exit, alt+f2, dota, phpstorm, youtube, f5
        assert len(executor._actions) == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
