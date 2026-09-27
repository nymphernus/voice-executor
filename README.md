# Голосовой ассистент

Приложение на Python для непрерывного распознавания речи с микрофона (офлайн) и выполнения голосовых команд.

## Структура проекта

```
voice-assistant/
├── main.py              # Точка входа
├── config.py            # Настройки и триггеры команд
├── commands.py          # Функции команд
├── recognizer.py        # Распознавание речи (Vosk)
├── executor.py          # Исполнитель команд
├── requirements.txt     # Зависимости
├── tests/               # Тесты
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_recognizer.py
│   └── test_executor.py
├── models/              # Модели Vosk (создаётся автоматически)
└── venv/                # Виртуальное окружение
```

## Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Добавление новой команды

Откройте `config.py` и добавьте триггер:

```python
TRIGGERS = {
    # ... существующие команды
    "новая_команда": "new_action",
}

GRAMMAR = [
    # ... существующие фразы
    "новая_команда",
]
```

Затем в `commands.py` добавьте функцию и зарегистрируйте её:

```python
def do_new_action():
    """Описание команды."""
    print("Выполняю новую команду...")

ACTIONS = {
    # ... существующие действия
    "new_action": do_new_action,
}
```

## Доступные команды

| Команда | Действие |
|---------|----------|
| "завершить", "стоп", "хватит" | Останавливает программу |
| "микрофон", "микро" | Alt+F2 (Discord) |
| "дота" | Запускает Dota 2 |
| "шторм", "storm" | Открывает PHPStorm |
| "ютуб", "youtube" | Открывает YouTube |
| "обновить", "обнови" | F5 (обновление страницы) |

## Тесты

```bash
pytest tests/ -v
```
