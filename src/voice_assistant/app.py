"""
Главный модуль приложения.
"""

import logging
import sys

from voice_assistant.commands import register_commands
from voice_assistant.config import load_config
from voice_assistant.executor import CommandExecutor
from voice_assistant.logging_setup import setup_logging
from voice_assistant.model_manager import ModelManager
from voice_assistant.nlu import NLUEngine
from voice_assistant.recognizer import SpeechRecognizer

logger = logging.getLogger(__name__)


def main() -> None:
    """Точка входа приложения."""
    # Логирование
    setup_logging()
    logger.info("=" * 50)
    logger.info("  Голосовой ассистент запущен")
    logger.info("=" * 50)

    # Конфигурация
    try:
        config = load_config()
        logger.info("Конфигурация загружена")
    except FileNotFoundError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        sys.exit(1)

    # Модель
    model_manager = ModelManager(config.recognition.model_path)
    try:
        model_path = model_manager.ensure_model()
    except RuntimeError as e:
        logger.error(f"Ошибка модели: {e}")
        sys.exit(1)

    # Распознаватель
    recognizer = SpeechRecognizer(config.recognition)
    recognizer.load_model()

    # NLU
    triggers = _build_triggers(config)
    nlu = NLUEngine(
        triggers=triggers,
        max_words=config.max_command_words,
    )

    # Executor
    executor = CommandExecutor()
    register_commands(executor)

    # Колбэк
    def on_recognized(text: str) -> None:
        logger.info(f"Распознано: {text}")
        result = nlu.match(text)
        if result.command:
            logger.info(
                f"Команда: {result.command} "
                f"(триггер: {result.trigger}, "
                f"confidence: {result.confidence:.2f})"
            )
            try:
                executor.execute(result.command)
            except KeyError as e:
                logger.error(f"Ошибка выполнения: {e}")
        else:
            logger.debug(f"Команда не распознана: {text}")

    # Запуск
    logger.info(f"Модель: {model_path}")
    logger.info(f"Триггеры: {list(triggers.keys())}")
    logger.info("Ctrl+C — остановка.")
    logger.info("")

    recognizer.start()
    recognizer.listen(on_final=on_recognized)


def _build_triggers(config) -> dict[str, str]:
    """Строит словарь триггеров из конфигурации."""
    triggers = {}
    cmd = config.commands

    for word in cmd.stop:
        triggers[word] = "exit"
    for word in cmd.discord:
        triggers[word] = "alt+f2"
    for word in cmd.dota:
        triggers[word] = "dota"
    for word in cmd.phpstorm:
        triggers[word] = "phpstorm"
    for word in cmd.youtube:
        triggers[word] = "youtube"
    for word in cmd.refresh:
        triggers[word] = "f5"

    return triggers


if __name__ == "__main__":
    main()
