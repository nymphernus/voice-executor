"""
Тесты для модуля recognizer.
"""

import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recognizer import (
    normalize_text,
    create_recognizer,
    create_audio_stream,
    listen_continuous,
)


class TestNormalizeText:
    """Тесты normalize_text."""

    def test_lowercase(self):
        assert normalize_text("СтОп") == "стоп"

    def test_strip(self):
        assert normalize_text("  стоп  ") == "стоп"

    def test_punctuation(self):
        assert normalize_text("стоп!") == "стоп"
        assert normalize_text("завершить.") == "завершить"


class TestCreateRecognizer:
    """Тесты create_recognizer."""

    @patch("recognizer.Model")
    @patch("recognizer.KaldiRecognizer")
    def test_create_recognizer(self, mock_rec_class, mock_model_class):
        mock_recognizer = MagicMock()
        mock_rec_class.return_value = mock_recognizer

        result = create_recognizer("fake_model_path")

        assert result == mock_recognizer
        mock_rec_class.assert_called_once()
        mock_recognizer.SetGrammar.assert_called_once()


class TestCreateAudioStream:
    """Тесты create_audio_stream."""

    @patch("recognizer.pyaudio.PyAudio")
    def test_create_stream(self, mock_pyaudio):
        mock_audio = MagicMock()
        mock_stream = MagicMock()
        mock_pyaudio.return_value = mock_audio
        mock_audio.open.return_value = mock_stream

        audio, stream = create_audio_stream()

        assert audio == mock_audio
        assert stream == mock_stream
        mock_audio.open.assert_called_once()


class TestListenContinuous:
    """Тесты listen_continuous."""

    @patch("recognizer.create_audio_stream")
    @patch("recognizer.create_recognizer")
    def test_keyboard_interrupt(self, mock_create_rec, mock_create_stream):
        mock_recognizer = MagicMock()
        mock_audio = MagicMock()
        mock_stream = MagicMock()

        mock_create_rec.return_value = mock_recognizer
        mock_create_stream.return_value = (mock_audio, mock_stream)
        mock_stream.read.side_effect = KeyboardInterrupt

        listen_continuous("fake_model_path")

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_audio.terminate.assert_called_once()

    @patch("recognizer.create_audio_stream")
    @patch("recognizer.create_recognizer")
    def test_with_callback(self, mock_create_rec, mock_create_stream):
        mock_recognizer = MagicMock()
        mock_audio = MagicMock()
        mock_stream = MagicMock()

        mock_create_rec.return_value = mock_recognizer
        mock_create_stream.return_value = (mock_audio, mock_stream)
        mock_recognizer.AcceptWaveform.side_effect = [True, False]
        mock_recognizer.Result.return_value = '{"text": "ютуб"}'
        mock_stream.read.side_effect = [b"data1", b"data2", KeyboardInterrupt]

        callback = MagicMock()
        listen_continuous("fake_model_path", on_recognized=callback)

        callback.assert_called_once_with("ютуб")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
