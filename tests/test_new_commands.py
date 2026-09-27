"""
Тесты для новых команд: диспетчер, терминал, скриншот, таймер.
"""

from unittest.mock import MagicMock, patch

import pytest

from voice_assistant.commands import system


class TestTaskManager:
    """Тесты диспетчера задач."""

    @patch("voice_assistant.commands.system.subprocess.Popen")
    def test_do_taskmanager(self, mock_popen):
        system.do_taskmanager()
        mock_popen.assert_called_once_with("taskmgr.exe", shell=True)


class TestTerminal:
    """Тесты терминала."""

    @patch("voice_assistant.commands.system.subprocess.Popen")
    @patch("voice_assistant.commands.system.platform.system")
    def test_do_terminal_windows_wt(self, mock_system, mock_popen):
        mock_system.return_value = "Windows"
        system.do_terminal()
        mock_popen.assert_called_once_with(["wt.exe"])

    @patch("voice_assistant.commands.system.subprocess.Popen")
    @patch("voice_assistant.commands.system.platform.system")
    def test_do_terminal_windows_cmd(self, mock_system, mock_popen):
        mock_system.return_value = "Windows"
        mock_popen.side_effect = [FileNotFoundError(), MagicMock()]
        system.do_terminal()
        assert mock_popen.call_count == 2

    @patch("voice_assistant.commands.system.subprocess.Popen")
    @patch("voice_assistant.commands.system.platform.system")
    def test_do_terminal_linux(self, mock_system, mock_popen):
        mock_system.return_value = "Linux"
        mock_popen.side_effect = FileNotFoundError()
        system.do_terminal()
        assert mock_popen.call_count == 4

    @patch("voice_assistant.commands.system.subprocess.Popen")
    @patch("voice_assistant.commands.system.platform.system")
    def test_do_terminal_macos(self, mock_system, mock_popen):
        mock_system.return_value = "Darwin"
        system.do_terminal()
        mock_popen.assert_called_once_with(["open", "-a", "Terminal"])


class TestScreenshot:
    """Тесты скриншота через Shift+Win+S."""

    @patch("voice_assistant.commands.system.platform.system")
    @patch("voice_assistant.commands.system.ctypes.windll.user32.keybd_event")
    def test_do_screenshot_windows(self, mock_keybd_event, mock_system):
        mock_system.return_value = "Windows"
        system.do_screenshot()
        # 6 вызовов: отпускаем Win, отпускаем S, нажимаем Win, Shift, S, отпускаем S, Shift, Win
        assert mock_keybd_event.call_count >= 6

    @patch("voice_assistant.commands.system.platform.system")
    def test_do_screenshot_not_windows(self, mock_system):
        mock_system.return_value = "Linux"
        # Не должно быть исключения
        system.do_screenshot()


class TestTimer:
    """Тесты таймера."""

    @patch("voice_assistant.commands.system.webbrowser.open")
    def test_do_timer_with_number(self, mock_open):
        system.do_timer("таймер 5 минут")
        mock_open.assert_called_once_with("https://www.google.com/search?q=5+minute+timer")

    @patch("voice_assistant.commands.system.webbrowser.open")
    def test_do_timer_with_word(self, mock_open):
        system.do_timer("таймер пять минут")
        mock_open.assert_called_once_with("https://www.google.com/search?q=5+minute+timer")

    @patch("voice_assistant.commands.system.webbrowser.open")
    def test_do_timer_without_number(self, mock_open):
        system.do_timer("таймер")
        mock_open.assert_called_once_with("https://www.google.com/search?q=timer")


class TestExtractMinutes:
    """Тесты извлечения минут."""

    def test_digit(self):
        assert system._extract_minutes("таймер 5 минут") == 5

    def test_word(self):
        assert system._extract_minutes("таймер пять минут") == 5

    def test_no_number(self):
        assert system._extract_minutes("таймер") is None

    def test_large_number(self):
        assert system._extract_minutes("таймер 30 минут") == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
