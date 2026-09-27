"""Работа с аудио: проверка микрофона, создание потока."""

import logging
from dataclasses import dataclass

import pyaudio

logger = logging.getLogger(__name__)


@dataclass
class AudioDevice:
    """Информация об аудиоустройстве."""
    index: int
    name: str
    max_input_channels: int
    default_sample_rate: float


def list_input_devices() -> list[AudioDevice]:
    """Возвращает список доступных устройств ввода (микрофонов)."""
    audio = pyaudio.PyAudio()
    devices = []

    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info.get("maxInputChannels", 0) > 0:
            devices.append(AudioDevice(
                index=i,
                name=info.get("name", f"Device {i}"),
                max_input_channels=info.get("maxInputChannels", 0),
                default_sample_rate=info.get("defaultSampleRate", 44100.0),
            ))

    audio.terminate()
    return devices


def check_microphone_available() -> bool:
    """Проверяет, доступен ли микрофон."""
    devices = list_input_devices()
    if not devices:
        logger.warning("Микрофон не найден")
        return False
    logger.info(f"Найдено микрофонов: {len(devices)}")
    for dev in devices:
        logger.debug(f"  [{dev.index}] {dev.name} ({dev.max_input_channels} каналов)")
    return True


def create_audio_stream(sample_rate: int = 16000, chunk_size: int = 4000, device: str = "default"):
    """
    Создаёт аудиопоток для записи с микрофона.

    Args:
        sample_rate: Частота дискретизации.
        chunk_size: Размер чанка.
        device: Индекс устройства или "default".

    Returns:
        Кортеж (PyAudio, Stream).

    Raises:
        RuntimeError: Если микрофон недоступен.
    """
    if not check_microphone_available():
        raise RuntimeError("Микрофон недоступен")

    audio = pyaudio.PyAudio()

    # Определяем индекс устройства
    device_index = None
    if device != "default":
        try:
            device_index = int(device)
        except ValueError:
            logger.warning(f"Некорректный индекс устройства: {device}, используется default")

    try:
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=chunk_size,
        )
        logger.info(f"Аудиопоток создан: {sample_rate} Hz, чанк {chunk_size}")
        return audio, stream
    except Exception as e:
        audio.terminate()
        raise RuntimeError(f"Не удалось открыть аудиопоток: {e}") from e
