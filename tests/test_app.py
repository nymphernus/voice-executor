"""
Тесты для модуля app.
"""

import pytest

from voice_assistant.app import _build_triggers
from voice_assistant.config import AppConfig, CommandsConfig, RecognitionConfig


class TestBuildTriggers:
    """Тесты построения триггеров."""

    def test_build_triggers(self):
        config = AppConfig(
            recognition=RecognitionConfig(),
            commands=CommandsConfig(
                stop=["стоп"],
                discord=["микрофон"],
                dota=["дота"],
                phpstorm=["шторм"],
                youtube=["ютуб"],
                refresh=["обновить"],
            ),
        )

        triggers = _build_triggers(config)

        assert triggers["стоп"] == "exit"
        assert triggers["микрофон"] == "alt+f2"
        assert triggers["дота"] == "dota"
        assert triggers["шторм"] == "phpstorm"
        assert triggers["ютуб"] == "youtube"
        assert triggers["обновить"] == "f5"

    def test_build_triggers_empty(self):
        config = AppConfig(
            recognition=RecognitionConfig(),
            commands=CommandsConfig(
                stop=[],
                discord=[],
                dota=[],
                phpstorm=[],
                youtube=[],
                refresh=[],
            ),
        )

        triggers = _build_triggers(config)
        # Новые команды имеют дефолтные триггеры
        assert "диспетчер" in triggers
        assert "терминал" in triggers
        assert "скриншот" in triggers
        assert "таймер" in triggers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
