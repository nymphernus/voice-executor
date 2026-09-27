"""
Тесты для модуля nlu.
"""

import pytest

from voice_assistant.nlu import NLUEngine


class TestNormalize:
    """Тесты нормализации текста."""

    def test_lowercase(self):
        nlu = NLUEngine()
        assert nlu.normalize("СтОп") == "стоп"

    def test_strip(self):
        nlu = NLUEngine()
        assert nlu.normalize("  стоп  ") == "стоп"

    def test_yo_to_e(self):
        nlu = NLUEngine()
        assert nlu.normalize("ёлка") == "елка"

    def test_extra_spaces(self):
        nlu = NLUEngine()
        assert nlu.normalize("стоп   что") == "стоп что"


class TestMatch:
    """Тесты сопоставления с триггерами."""

    def test_exact_match(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers)
        result = nlu.match("стоп")
        assert result.command == "exit"
        assert result.trigger == "стоп"
        assert result.confidence == 1.0

    def test_partial_match(self):
        triggers = {"микрофон": "alt+f2"}
        nlu = NLUEngine(triggers=triggers)
        result = nlu.match("включи микрофон")
        assert result.command == "alt+f2"

    def test_no_match(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers)
        result = nlu.match("какая погода")
        assert result.command is None

    def test_max_words_protection(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers, max_words=2)
        result = nlu.match("стоп что ты делаешь")
        assert result.command is None

    def test_debounce(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers, debounce_seconds=10.0)

        # Первый вызов — срабатывает
        result1 = nlu.match("стоп")
        assert result1.command == "exit"

        # Второй вызов сразу — не срабатывает (антидребезг)
        result2 = nlu.match("стоп")
        assert result2.command is None

    def test_different_commands_no_debounce(self):
        triggers = {"стоп": "exit", "дота": "dota"}
        nlu = NLUEngine(triggers=triggers, debounce_seconds=10.0)

        result1 = nlu.match("стоп")
        assert result1.command == "exit"

        # Другая команда — срабатывает
        result2 = nlu.match("дота")
        assert result2.command == "dota"


class TestFuzzyMatch:
    """Тесты fuzzy matching."""

    def test_fuzzy_match(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers, fuzzy_threshold=0.7)
        result = nlu.match("стоп")
        assert result.command == "exit"

    def test_fuzzy_no_match(self):
        triggers = {"стоп": "exit"}
        nlu = NLUEngine(triggers=triggers, fuzzy_threshold=0.9)
        result = nlu.match("совершенно другое слово")
        assert result.command is None


class TestLevenshtein:
    """Тесты расстояния Левенштейна."""

    def test_identical(self):
        assert NLUEngine._levenshtein_ratio("стоп", "стоп") == 1.0

    def test_completely_different(self):
        assert NLUEngine._levenshtein_ratio("abc", "xyz") == 0.0

    def test_similar(self):
        ratio = NLUEngine._levenshtein_ratio("стоп", "сток")
        assert 0.5 < ratio < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
