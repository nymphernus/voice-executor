"""
Распознавание речи через Vosk.
"""

import json
import string

import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel

from config import SAMPLE_RATE, CHUNK_SIZE, GRAMMAR

SetLogLevel(-1)


def normalize_text(text: str) -> str:
    """Удаляет пунктуацию и приводит к нижнему регистру."""
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def create_recognizer(model_path: str):
    """Создаёт распознаватель Vosk."""
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)
    recognizer.SetPartialWords(True)

    # Устанавливаем грамматику для улучшения распознавания
    recognizer.SetGrammar(json.dumps(GRAMMAR, ensure_ascii=False))

    return recognizer


def create_audio_stream():
    """Создаёт аудиопоток для записи с микрофона."""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )
    return audio, stream


def listen_continuous(model_path: str, on_recognized=None):
    """
    Непрерывно прослушивает микрофон и распознаёт речь.

    Args:
        model_path: Путь к модели Vosk.
        on_recognized: Колбэк, вызываемый с распознанным текстом.
    """
    recognizer = create_recognizer(model_path)
    audio, stream = create_audio_stream()

    try:
        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text and on_recognized:
                    on_recognized(text)
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
