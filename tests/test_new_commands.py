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
        mock_popen.assert_called_once_with(["taskmgr.exe"])

    @patch("voice_assistant.commands.system.subprocess.Popen")
    def test_do_taskmanager_not_found(self, mock_popen):
        mock_popen.side_effect = FileNotFoundError()
        system.do_taskmanager()


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
    """Тесты скриншота."""

    @patch.dict("sys.modules", {"PIL": MagicMock(), "PIL.ImageGrab": MagicMock()})
    def test_do_screenshot(self):
        from PIL import ImageGrab

        mock_screenshot = MagicMock()
        ImageGrab.grab.return_value = mock_screenshot

        system.do_screenshot()

        ImageGrab.grab.assert_called_once()
        mock_screenshot.save.assert_called_once()

    def test_do_screenshot_no_pillow(self):
        with patch.dict("sys.modules", {"PIL": None, "PIL.ImageGrab": None}):
            system.do_screenshot()


class TestTimer:
    """Тесты таймера."""

    @patch("voice_assistant.commands.system.webbrowser.open")
    def test_do_timer(self, mock_open):
        system.do_timer()
        mock_open.assert_called_once_with("https://www.google.com/search?q=timer")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
