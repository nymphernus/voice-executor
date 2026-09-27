"""
Тесты для модуля model_manager.
"""

from unittest.mock import MagicMock, patch

import pytest

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

    @patch("voice_assistant.model_manager.zipfile.ZipFile")
    @patch("voice_assistant.model_manager.urllib.request.urlopen")
    def test_download(self, mock_urlopen, mock_zipfile_class, tmp_path):
        # Мокаем HTTP-ответ
        mock_response = MagicMock()
        mock_response.headers = {"Content-Length": "1024"}
        mock_response.read.side_effect = [b"x" * 512, b"x" * 512, b""]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        mock_zip = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zip

        manager = ModelManager(str(tmp_path / "vosk-model-small-ru-0.22"))
        result = manager.download()

        mock_urlopen.assert_called_once()
        mock_zip.extractall.assert_called_once()
        assert result == tmp_path / "vosk-model-small-ru-0.22"

    def test_ensure_model_exists(self, tmp_path):
        model_dir = tmp_path / "vosk-model-small-ru-0.22"
        model_dir.mkdir()
        manager = ModelManager(str(model_dir))
        result = manager.ensure_model()
        assert result == model_dir

    @patch("voice_assistant.model_manager.zipfile.ZipFile")
    @patch("voice_assistant.model_manager.urllib.request.urlopen")
    def test_ensure_model_download(self, mock_urlopen, mock_zipfile_class, tmp_path):
        # Мокаем HTTP-ответ
        mock_response = MagicMock()
        mock_response.headers = {"Content-Length": "1024"}
        mock_response.read.side_effect = [b"x" * 512, b"x" * 512, b""]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        mock_zip = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zip

        manager = ModelManager(str(tmp_path / "vosk-model-small-ru-0.22"))
        result = manager.ensure_model()

        mock_urlopen.assert_called_once()
        assert result == tmp_path / "vosk-model-small-ru-0.22"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
