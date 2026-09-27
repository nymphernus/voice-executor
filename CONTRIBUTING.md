# Contributing

## Установка для разработки

```bash
git clone https://github.com/your-repo/voice-executor.git
cd voice-executor
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Запуск тестов

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing
```

## Линтеры

```bash
ruff check src tests
black src tests
mypy src/voice_assistant
```

## Добавление новой команды

1. Добавьте триггер в `config.toml` в секцию `[commands]`
2. Создайте функцию в `src/voice_assistant/commands/`
3. Зарегистрируйте в `src/voice_assistant/commands/__init__.py`
4. Добавьте тесты в `tests/`

## Стиль кода

- Python 3.10+
- Типизация обязательна
- Docstring для всех публичных функций
- Лимит строки: 100 символов
