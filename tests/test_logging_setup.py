"""
Тесты для модуля logging_setup.
"""

import logging

import pytest

from voice_assistant.logging_setup import setup_logging


class TestSetupLogging:
    """Тесты настройки логирования."""

    def test_setup_logging(self, tmp_path):
        logger = setup_logging(
            log_dir=str(tmp_path / "logs"),
            log_file="test.log",
            level=logging.DEBUG,
        )

        assert logger.name == "voice_assistant"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) >= 2  # консоль + файл

    def test_log_file_created(self, tmp_path):
        log_dir = tmp_path / "logs"
        logger = setup_logging(
            log_dir=str(log_dir),
            log_file="test.log",
        )

        # Пишем тестовое сообщение
        logger.info("Test message")

        # Проверяем, что файл создан
        log_file = log_dir / "test.log"
        assert log_file.exists()

    def test_log_rotation(self, tmp_path):
        logger = setup_logging(
            log_dir=str(tmp_path / "logs"),
            log_file="test.log",
            max_bytes=100,  # Маленький размер для теста
            backup_count=2,
        )

        # Пишем много сообщений для ротации
        for i in range(100):
            logger.info(f"Test message {i}" * 10)

        # Проверяем, что файл создан
        log_file = tmp_path / "logs" / "test.log"
        assert log_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
