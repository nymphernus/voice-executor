"""
Тесты для модуля recognizer.
"""

import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

from voice_assistant.recognizer import SpeechRecognizer
from voice_assistant.config import RecognitionConfig


class TestSpeechRecognizer:
    """Тесты SpeechRecognizer."""

    def test_init(self):
        config = RecognitionConfig()
        recognizer = SpeechRecognizer(config)
        assert recognizer.config == config

    @patch("voice_assistant.recognizer.KaldiRecognizer")
    @patch("voice_assistant.recognizer.Model")
    def test_load_model(self, mock_model_class, mock_rec_class):
        config = RecognitionConfig()
        recognizer = SpeechRecognizer(config)
        recognizer.load_model()
        mock_model_class.assert_called_once_with(config.model_path)
        mock_rec_class.assert_called_once()

    @patch("voice_assistant.recognizer.create_audio_stream")
    def test_start(self, mock_create_stream):
        config = RecognitionConfig()
        recognizer = SpeechRecognizer(config)

        mock_audio = MagicMock()
        mock_stream = MagicMock()
        mock_create_stream.return_value = (mock_audio, mock_stream)

        recognizer.start()
        assert recognizer._audio == mock_audio
        assert recognizer._stream == mock_stream

    def test_stop(self):
        config = RecognitionConfig()
        recognizer = SpeechRecognizer(config)

        mock_audio = MagicMock()
        mock_stream = MagicMock()
        recognizer._audio = mock_audio
        recognizer._stream = mock_stream

        recognizer.stop()
        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_audio.terminate.assert_called_once()

    @patch("voice_assistant.recognizer.create_audio_stream")
    def test_listen_keyboard_interrupt(self, mock_create_stream):
        config = RecognitionConfig()
        recognizer = SpeechRecognizer(config)

        mock_audio = MagicMock()
        mock_stream = MagicMock()
        mock_create_stream.return_value = (mock_audio, mock_stream)
        mock_stream.read.side_effect = KeyboardInterrupt

        recognizer._recognizer = MagicMock()
        recognizer._stream = mock_stream
        recognizer.listen(on_final=MagicMock())

        mock_stream.stop_stream.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
