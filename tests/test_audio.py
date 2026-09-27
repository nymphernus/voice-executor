"""
Тесты для модуля audio.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

from voice_assistant.audio import (
    list_input_devices,
    check_microphone_available,
    create_audio_stream,
    AudioDevice,
)


class TestListInputDevices:
    """Тесты списка устройств."""

    @patch("voice_assistant.audio.pyaudio.PyAudio")
    def test_list_devices(self, mock_pyaudio_class):
        mock_audio = MagicMock()
        mock_pyaudio_class.return_value = mock_audio

        # Мокаем два устройства
        mock_audio.get_device_count.return_value = 2
        mock_audio.get_device_info_by_index.side_effect = [
            {"maxInputChannels": 1, "name": "Mic 1", "defaultSampleRate": 44100.0},
            {"maxInputChannels": 0, "name": "Speaker", "defaultSampleRate": 44100.0},
        ]

        devices = list_input_devices()

        assert len(devices) == 1
        assert devices[0].name == "Mic 1"
        assert devices[0].max_input_channels == 1


class TestCheckMicrophone:
    """Тесты проверки микрофона."""

    @patch("voice_assistant.audio.list_input_devices")
    def test_available(self, mock_list):
        mock_list.return_value = [AudioDevice(0, "Mic", 1, 44100.0)]
        assert check_microphone_available() is True

    @patch("voice_assistant.audio.list_input_devices")
    def test_not_available(self, mock_list):
        mock_list.return_value = []
        assert check_microphone_available() is False


class TestCreateAudioStream:
    """Тесты создания аудиопотока."""

    @patch("voice_assistant.audio.check_microphone_available")
    @patch("voice_assistant.audio.pyaudio.PyAudio")
    def test_create_stream(self, mock_pyaudio_class, mock_check):
        mock_check.return_value = True

        mock_audio = MagicMock()
        mock_stream = MagicMock()
        mock_pyaudio_class.return_value = mock_audio
        mock_audio.open.return_value = mock_stream

        audio, stream = create_audio_stream(sample_rate=16000, chunk_size=4000)

        assert audio == mock_audio
        assert stream == mock_stream
        mock_audio.open.assert_called_once()

    @patch("voice_assistant.audio.check_microphone_available")
    def test_no_microphone(self, mock_check):
        mock_check.return_value = False
        with pytest.raises(RuntimeError):
            create_audio_stream()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
