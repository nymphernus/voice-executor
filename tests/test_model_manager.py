"""
Тесты для модуля model_manager.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from voice_assistant.model_manager import ModelManager


class TestModelManager:
    """Тесты ModelManager."""

    def test_exists_true(self, tmp_path):
        model_dir = tmp_path / "vosk-model-small-ru-0.22"
        model_dir.mkdir()
        manager = ModelManager(str(model_dir))
        assert manager.exists() is True

    def test_exists_false(self, tmp_path):
        manager = ModelManager(str(tmp_path / "nonexistent"))
        assert manager.exists() is False

    @patch("voice_assistant.model_manager.urllib.request.urlretrieve")
    @patch("voice_assistant.model_manager.zipfile.ZipFile")
    def test_download(self, mock_zipfile_class, mock_urlretrieve, tmp_path):
        # Создаём фейковый ZIP
        zip_path = tmp_path / "model.zip"
        zip_path.write_bytes(b"fake zip content")

        mock_zip = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zip

        manager = ModelManager(str(tmp_path / "vosk-model-small-ru-0.22"))
        result = manager.download()

        mock_urlretrieve.assert_called_once()
        mock_zip.extractall.assert_called_once()
        assert result == tmp_path / "vosk-model-small-ru-0.22"

    def test_ensure_model_exists(self, tmp_path):
        model_dir = tmp_path / "vosk-model-small-ru-0.22"
        model_dir.mkdir()
        manager = ModelManager(str(model_dir))
        result = manager.ensure_model()
        assert result == model_dir

    @patch("voice_assistant.model_manager.urllib.request.urlretrieve")
    @patch("voice_assistant.model_manager.zipfile.ZipFile")
    def test_ensure_model_download(self, mock_zipfile_class, mock_urlretrieve, tmp_path):
        zip_path = tmp_path / "model.zip"
        zip_path.write_bytes(b"fake zip content")

        mock_zip = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zip

        manager = ModelManager(str(tmp_path / "vosk-model-small-ru-0.22"))
        result = manager.ensure_model()

        mock_urlretrieve.assert_called_once()
        assert result == tmp_path / "vosk-model-small-ru-0.22"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
