"""
Тесты для модуля commands.
"""

from unittest.mock import patch

import pytest

from voice_assistant.commands import apps, browser, discord, system


class TestSystemCommands:
    """Тесты системных команд."""

    def test_do_exit(self):
        with pytest.raises(SystemExit) as exc_info:
            system.do_exit()
        assert exc_info.value.code == 0

    @patch("voice_assistant.commands.system.ctypes.windll.user32.keybd_event")
    def test_do_f5(self, mock_keybd_event):
        system.do_f5()
        assert mock_keybd_event.call_count == 2


class TestBrowserCommands:
    """Тесты команд браузера."""

    @patch("voice_assistant.commands.browser.webbrowser.open")
    def test_do_youtube(self, mock_open):
        browser.do_youtube()
        mock_open.assert_called_once_with("https://www.youtube.com")


class TestAppsCommands:
    """Тесты команд приложений."""

    @patch("voice_assistant.commands.apps.webbrowser.open")
    def test_do_dota(self, mock_open):
        apps.do_dota()
        mock_open.assert_called_once_with("steam://rungameid/570")

    @patch("voice_assistant.commands.apps._find_phpstorm")
    def test_do_phpstorm_found(self, mock_find):
        mock_find.return_value = r"C:\PhpStorm\bin\phpstorm64.exe"

        with patch("voice_assistant.commands.apps.subprocess.Popen") as mock_popen:
            apps.do_phpstorm()
            mock_popen.assert_called_once()

    @patch("voice_assistant.commands.apps._find_phpstorm")
    def test_do_phpstorm_not_found(self, mock_find):
        mock_find.return_value = None
        apps.do_phpstorm()


class TestDiscordCommands:
    """Тесты команд Discord."""

    @patch("voice_assistant.commands.discord.ctypes.windll.user32.keybd_event")
    def test_do_alt_f2(self, mock_keybd_event):
        discord.do_alt_f2()
        assert mock_keybd_event.call_count == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
