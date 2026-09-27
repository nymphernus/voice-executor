"""
NLU — обработка естественного языка.

Нормализация, сопоставление с триггерами, fuzzy matching, антидребезг.
"""

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    """Результат сопоставления текста с командой."""
    command: str | None = None
    trigger: str | None = None
    confidence: float = 0.0


@dataclass
class NLUEngine:
    """Движок обработки естественного языка."""

    triggers: dict[str, str] = field(default_factory=dict)
    max_words: int = 2
    debounce_seconds: float = 1.0
    fuzzy_threshold: float = 0.8

    def __post_init__(self):
        self._last_command: str | None = None
        self._last_time: float = 0.0

    def normalize(self, text: str) -> str:
        """
        Нормализует текст: нижний регистр, ё->е, убрать лишние пробелы.

        Args:
            text: Исходный текст.

        Returns:
            Нормализованный текст.
        """
        text = text.lower().strip()
        text = text.replace("ё", "е")
        # Убрать лишние пробелы
        text = " ".join(text.split())
        return text

    def match(self, text: str) -> MatchResult:
        """
        Сопоставляет текст с триггерами команд.

        Args:
            text: Распознанный текст.

        Returns:
            Результат сопоставления.
        """
        normalized = self.normalize(text)
        words = normalized.split()

        # Защита: если слов больше max_words — пропускаем
        if len(words) > self.max_words:
            return MatchResult()

        # Точное совпадение
        if normalized in self.triggers:
            return self._check_debounce(
                MatchResult(command=self.triggers[normalized], trigger=normalized, confidence=1.0)
            )

        # Поиск триггера внутри текста
        for trigger, command in self.triggers.items():
            if trigger in normalized:
                return self._check_debounce(
                    MatchResult(command=command, trigger=trigger, confidence=0.9)
                )

        # Fuzzy matching
        best_match = self._fuzzy_match(normalized)
        if best_match:
            return self._check_debounce(best_match)

        return MatchResult()

    def _check_debounce(self, result: MatchResult) -> MatchResult:
        """
        Проверяет антидребезг: не выполнять одну команду несколько раз подряд.

        Args:
            result: Результат сопоставления.

        Returns:
            Результат или пустой, если команда уже выполнялась недавно.
        """
        now = time.time()

        if result.command == self._last_command:
            if now - self._last_time < self.debounce_seconds:
                logger.debug(f"Антидребезг: команда '{result.command}' уже выполнялась")
                return MatchResult()

        self._last_command = result.command
        self._last_time = now
        return result

    def _fuzzy_match(self, text: str) -> MatchResult | None:
        """
        Находит лучшее совпадение по fuzzy matching.

        Args:
            text: Нормализованный текст.

        Returns:
            Результат или None.
        """
        best_command = None
        best_trigger = None
        best_ratio = 0.0

        for trigger, command in self.triggers.items():
            ratio = self._levenshtein_ratio(text, trigger)
            if ratio > best_ratio:
                best_ratio = ratio
                best_command = command
                best_trigger = trigger

        if best_ratio >= self.fuzzy_threshold:
            return MatchResult(
                command=best_command,
                trigger=best_trigger,
                confidence=best_ratio,
            )
        return None

    @staticmethod
    def _levenshtein_ratio(s1: str, s2: str) -> float:
        """
        Вычисляет коэффициент похожести двух строк (0.0 — 1.0).

        Args:
            s1: Первая строка.
            s2: Вторая строка.

        Returns:
            Коэффициент похожести.
        """
        if not s1 or not s2:
            return 0.0

        # Расстояние Левенштейна
        len1, len2 = len(s1), len(s2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,      # удаление
                    matrix[i][j - 1] + 1,      # вставка
                    matrix[i - 1][j - 1] + cost  # замена
                )

        distance = matrix[len1][len2]
        max_len = max(len1, len2)
        return 1.0 - (distance / max_len) if max_len > 0 else 1.0
