"""
Тесты для модуля config.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    MODEL_PATH,
    SAMPLE_RATE,
    CHUNK_SIZE,
    MAX_COMMAND_WORDS,
    TRIGGERS,
    GRAMMAR,
)


class TestConfig:
    """Тесты конфигурации."""

    def test_model_path(self):
        assert MODEL_PATH == "models/vosk-model-small-ru-0.22"

    def test_sample_rate(self):
        assert SAMPLE_RATE == 16000

    def test_chunk_size(self):
        assert CHUNK_SIZE == 4000

    def test_max_command_words(self):
        assert MAX_COMMAND_WORDS == 2


class TestTriggers:
    """Тесты триггеров."""

    def test_triggers_not_empty(self):
        assert len(TRIGGERS) > 0

    def test_has_exit_triggers(self):
        exit_words = ["завершить", "заверши", "стоп", "хватит", "выключи", "конец", "отмена"]
        for word in exit_words:
            assert word in TRIGGERS, f"Нет триггера: {word}"
            assert TRIGGERS[word] == "exit"

    def test_has_microphone_triggers(self):
        mic_words = ["микрофон", "микро"]
        for word in mic_words:
            assert word in TRIGGERS, f"Нет триггера: {word}"
            assert TRIGGERS[word] == "alt+f2"

    def test_has_dota(self):
        assert "дота" in TRIGGERS
        assert TRIGGERS["дота"] == "steam://rungameid/570"

    def test_has_phpstorm_triggers(self):
        php_words = ["шторм", "storm"]
        for word in php_words:
            assert word in TRIGGERS, f"Нет триггера: {word}"
            assert TRIGGERS[word] == "phpstorm"

    def test_has_youtube_triggers(self):
        yt_words = ["ютуб", "youtube"]
        for word in yt_words:
            assert word in TRIGGERS, f"Нет триггера: {word}"
            assert TRIGGERS[word] == "https://www.youtube.com"

    def test_has_refresh_triggers(self):
        refresh_words = ["обновить", "обнови", "обновление"]
        for word in refresh_words:
            assert word in TRIGGERS, f"Нет триггера: {word}"
            assert TRIGGERS[word] == "f5"

    def test_no_steam(self):
        assert "стим" not in TRIGGERS

    def test_no_google(self):
        assert "гугл" not in TRIGGERS
        assert "google" not in TRIGGERS


class TestGrammar:
    """Тесты грамматики."""

    def test_grammar_not_empty(self):
        assert len(GRAMMAR) > 0

    def test_grammar_has_all_triggers(self):
        for trigger in TRIGGERS:
            assert any(trigger in phrase for phrase in GRAMMAR), f"Нет в грамматике: {trigger}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
