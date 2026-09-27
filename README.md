# Voice Executor

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
git clone https://github.com/your-repo/voice-executor.git
cd voice-executor

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
voice-executor

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
taskmanager = ["диспетчер"]
terminal = ["терминал"]
screenshot = ["скриншот"]
timer = ["таймер"]

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
| "шторм" | Открывает PHPStorm |
| "ютуб" | Открывает YouTube |
| "обновить", "обнови" | F5 (обновление страницы) |
| "диспетчер" | Открывает диспетчер задач |
| "терминал" | Открывает терминал |
| "скриншот" | Делает скриншот через Shift+Win+S |
| "таймер N" | Открывает таймер на N минут в браузере |

### Примеры таймера

```
"таймер 5 минут"     → google.com/search?q=5+minute+timer
"таймер пять минут"  → google.com/search?q=5+minute+timer
"таймер 30 минут"    → google.com/search?q=30+minute+timer
"таймер"              → google.com/search?q=timer
```

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
voice-executor/
├── main.py              # Тонкая обёртка
├── config.example.toml  # Пример конфигурации
├── pyproject.toml       # Сборка и зависимости
├── src/voice_assistant/ # Исходный код
│   ├── app.py           # Главный модуль
│   ├── config.py        # TOML-конфигурация
│   ├── logging_setup.py # Логирование
│   ├── audio.py         # Работа с микрофоном
│   ├── recognizer.py     # Распознавание (Vosk)
│   ├── nlu.py            # NLU: нормализация, fuzzy, антидребезг
│   ├── executor.py       # Реестр действий
│   ├── model_manager.py  # Управление моделью
│   └── commands/         # Команды
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

## Ссборка exe (Windows)

```bash
pip install pyinstaller
pyinstaller voice-executor.spec --clean
```

Или через скрипт:
```bash
python scripts/build_exe.py
```

### Важно для работы exe

1. **config.toml** — скопируйте `config.example.toml` рядом с exe и переименуйте в `config.toml`
2. **Модель Vosk** — скачайте и положите папку `models/` рядом с exe:
   ```bash
   python scripts/download_model.py
   ```
3. **Логи** — будут сохраняться в `logs/` рядом с exe

### Структура для распространения

```
dist/
├── voice-executor.exe
├── config.toml          # скопировать из config.example.toml
├── models/              # скачать через scripts/download_model.py
│   └── vosk-model-small-ru-0.22/
└── logs/                # создаётся автоматически
```

## Troubleshooting

### Микрофон не найден
- Проверьте, что микрофон подключён и не занят другим приложением
- Проверьте настройки конфиденциальности Windows (Доступ к микрофону)

### Модель не скачивается
- Проверьте подключение к интернету
- Скачайте вручную: https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
- Распакуйте в `models/`

### Команды не срабатывают
- Говорите чётко и не слишком быстро
- Увеличьте `max_command_words` в конфиге, если нужно
- Проверьте логи в `logs/assistant.log`