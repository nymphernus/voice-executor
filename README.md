# Voice Assistant

Офлайн голосовой ассистент на Python с распознаванием речи через Vosk.

## Возможности

- Непрерывное распознавание речи с микрофона (офлайн)
- Выполнение голосовых команд
- Fuzzy matching для устойчивости к ошибкам распознавания
- Антидребезг (защита от повторного срабатывания)
- TOML-конфигурация
- Логирование (консоль + файл с ротацией)
- Расширяемая система команд

## Требования

- Python 3.10+
- Микрофон
- ~50 MB места на диске (для модели)

## Установка

```bash
# Клонирование
git clone https://github.com/your-repo/voice-assistant.git
cd voice-assistant

# Виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Установка
pip install -e .
```

## Скачивание модели

```bash
# Маленькая модель (~50 MB)
python scripts/download_model.py

# Или большая модель (~1.5 GB) для лучшего распознавания
python scripts/download_model.py --model big
```

## Запуск

```bash
# Через Python
python main.py

# Или через entry point
voice-assistant

# Или как модуль
python -m voice_assistant
```

## Настройка

Скопируйте `config.example.toml` в `config.toml` и настройте под себя:

```toml
[recognition]
model_path = "models/vosk-model-small-ru-0.22"
sample_rate = 16000
chunk_size = 4000
device = "default"

[commands]
stop = ["завершить", "стоп", "хватит"]
discord = ["микрофон", "микро"]
dota = ["дота"]
phpstorm = ["шторм", "storm"]
youtube = ["ютуб", "youtube"]
refresh = ["обновить", "обнови"]

max_command_words = 2
```

### Переменные окружения

- `VA_MODEL_PATH` — переопределяет путь к модели
- `VA_SAMPLE_RATE` — переопределяет частоту дискретизации

## Доступные команды

| Команда | Действие |
|---------|----------|
| "завершить", "стоп", "хватит" | Останавливает программу |
| "микрофон", "микро" | Alt+F2 в Discord |
| "дота" | Запускает Dota 2 |
| "шторм", "storm" | Открывает PHPStorm |
| "ютуб", "youtube" | Открывает YouTube |
| "обновить", "обнови" | F5 (обновление страницы) |

## Добавление новой команды

1. Откройте `config.toml` и добавьте триггер в секцию `[commands]`:

```toml
[commands]
my_command = ["триггер1", "триггер2"]
```

2. В `src/voice_assistant/commands/` создайте функцию:

```python
def do_my_command() -> None:
    """Описание команды."""
    print("Выполняю команду...")
```

3. Зарегистрируйте в `src/voice_assistant/commands/__init__.py`:

```python
executor.register("my_command", my_module.do_my_command)
```

## Структура проекта

```
voice-assistant/
├── main.py              # Тонкая обёртка
├── config.example.toml  # Пример конфигурации
├── pyproject.toml       # Сборка и зависимости
├── src/voice_assistant/ # Исходный код
├── tests/               # Тесты
├── scripts/             # Скрипты
├── models/              # Модели Vosk (не в Git)
└── logs/                # Логи (не в Git)
```

## Тесты

```bash
# Все тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=src --cov-report=term-missing
```

## Сборка exe (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --name voice-assistant main.py
```

## Лицензия

MIT
