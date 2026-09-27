"""
Конфигурация приложения через TOML.

Загружается из config.toml или config.example.toml.
Поддерживает переопределение через переменные окружения.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@dataclass
class RecognitionConfig:
    """Настройки распознавания речи."""
    model_path: str = "models/vosk-model-small-ru-0.22"
    sample_rate: int = 16000
    chunk_size: int = 4000
    device: str = "default"


@dataclass
class CommandsConfig:
    """Триггеры команд."""
    stop: list[str] = field(default_factory=lambda: ["завершить", "стоп", "хватит"])
    discord: list[str] = field(default_factory=lambda: ["микрофон", "микро"])
    dota: list[str] = field(default_factory=lambda: ["дота"])
    phpstorm: list[str] = field(default_factory=lambda: ["шторм", "storm"])
    youtube: list[str] = field(default_factory=lambda: ["ютуб", "youtube"])
    refresh: list[str] = field(default_factory=lambda: ["обновить", "обнови"])


@dataclass
class AppConfig:
    """Главная конфигурация."""
    recognition: RecognitionConfig = field(default_factory=RecognitionConfig)
    commands: CommandsConfig = field(default_factory=CommandsConfig)
    max_command_words: int = 2


def load_config(config_path: str | Path | None = None) -> AppConfig:
    """
    Загружает конфигурацию из TOML-файла.

    Args:
        config_path: Путь к файлу конфигурации. Если None — ищет config.toml.

    Returns:
        Объект конфигурации.

    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
        ValueError: Если конфигурация невалидна.
    """
    if config_path is None:
        # Ищем config.toml в текущей директории
        config_path = Path("config.toml")
        if not config_path.exists():
            config_path = Path("config.example.toml")
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Конфигурация не найдена: {config_path}\n"
            f"Создайте config.toml на основе config.example.toml"
        )

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    # Распознавание
    rec_data = data.get("recognition", {})
    recognition = RecognitionConfig(
        model_path=rec_data.get("model_path", "models/vosk-model-small-ru-0.22"),
        sample_rate=rec_data.get("sample_rate", 16000),
        chunk_size=rec_data.get("chunk_size", 4000),
        device=rec_data.get("device", "default"),
    )

    # Команды
    cmd_data = data.get("commands", {})
    commands = CommandsConfig(
        stop=cmd_data.get("stop", ["завершить", "стоп", "хватит"]),
        discord=cmd_data.get("discord", ["микрофон", "микро"]),
        dota=cmd_data.get("dota", ["дота"]),
        phpstorm=cmd_data.get("phpstorm", ["шторм", "storm"]),
        youtube=cmd_data.get("youtube", ["ютуб", "youtube"]),
        refresh=cmd_data.get("refresh", ["обновить", "обнови"]),
    )

    # Переопределение через переменные окружения
    if os.getenv("VA_MODEL_PATH"):
        recognition.model_path = os.getenv("VA_MODEL_PATH")
    if os.getenv("VA_SAMPLE_RATE"):
        recognition.sample_rate = int(os.getenv("VA_SAMPLE_RATE"))

    max_words = data.get("max_command_words", 2)

    return AppConfig(
        recognition=recognition,
        commands=commands,
        max_command_words=max_words,
    )
