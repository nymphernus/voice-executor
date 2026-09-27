"""
Тесты для модуля config.
"""

import os
import sys
import pytest
from pathlib import Path

from voice_assistant.config import (
    load_config,
    AppConfig,
    RecognitionConfig,
    CommandsConfig,
)


class TestLoadConfig:
    """Тесты загрузки конфигурации."""

    def test_load_default(self, tmp_path):
        """Загрузка конфигурации по умолчанию."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("""
[recognition]
model_path = "models/test"
sample_rate = 16000
chunk_size = 4000
device = "default"

[commands]
stop = ["стоп"]
discord = ["микрофон"]
dota = ["дота"]
phpstorm = ["шторм"]
youtube = ["ютуб"]
refresh = ["обновить"]

max_command_words = 2
""", encoding="utf-8")

        config = load_config(config_file)

        assert isinstance(config, AppConfig)
        assert config.recognition.model_path == "models/test"
        assert config.recognition.sample_rate == 16000
        assert config.commands.stop == ["стоп"]
        assert config.max_command_words == 2

    def test_load_example(self):
        """Загрузка примера конфигурации."""
        config = load_config("config.example.toml")

        assert isinstance(config, AppConfig)
        assert config.recognition.model_path == "models/vosk-model-small-ru-0.22"
        assert config.commands.stop == ["завершить", "стоп", "хватит"]

    def test_file_not_found(self, tmp_path):
        """Ошибка при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            load_config(tmp_path / "nonexistent.toml")

    def test_env_override(self, tmp_path, monkeypatch):
        """Переопределение через переменные окружения."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("""
[recognition]
model_path = "models/test"
sample_rate = 16000
chunk_size = 4000
device = "default"

[commands]
stop = ["стоп"]
discord = ["микрофон"]
dota = ["дота"]
phpstorm = ["шторм"]
youtube = ["ютуб"]
refresh = ["обновить"]
""", encoding="utf-8")

        monkeypatch.setenv("VA_MODEL_PATH", "models/custom")
        monkeypatch.setenv("VA_SAMPLE_RATE", "8000")

        config = load_config(config_file)

        assert config.recognition.model_path == "models/custom"
        assert config.recognition.sample_rate == 8000


class TestRecognitionConfig:
    """Тесты конфигурации распознавания."""

    def test_defaults(self):
        config = RecognitionConfig()
        assert config.model_path == "models/vosk-model-small-ru-0.22"
        assert config.sample_rate == 16000
        assert config.chunk_size == 4000
        assert config.device == "default"


class TestCommandsConfig:
    """Тесты конфигурации команд."""

    def test_defaults(self):
        config = CommandsConfig()
        assert "стоп" in config.stop
        assert "микрофон" in config.discord
        assert "дота" in config.dota
        assert "шторм" in config.phpstorm
        assert "ютуб" in config.youtube
        assert "обновить" in config.refresh


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
