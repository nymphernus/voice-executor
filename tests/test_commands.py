"""
Тесты для модуля commands.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commands import (
    do_exit,
    do_alt_f2,
    do_dota,
    do_f5,
    do_youtube,
    find_phpstorm,
    get_all_drives,
    ACTIONS,
)


class TestDoExit:
    """Тесты do_exit."""

    @patch("commands.sys.exit")
    def test_exit(self, mock_exit):
        do_exit()
        mock_exit.assert_called_once_with(0)


class TestDoAltF2:
    """Тесты do_alt_f2."""

    @patch("commands.ctypes.windll.user32.keybd_event")
    def test_alt_f2(self, mock_keybd_event):
        do_alt_f2()
        assert mock_keybd_event.call_count == 4


class TestDoDota:
    """Тесты do_dota."""

    @patch("commands.webbrowser.open")
    def test_dota(self, mock_open):
        do_dota()
        mock_open.assert_called_once_with("steam://rungameid/570")


class TestDoYoutube:
    """Тесты do_youtube."""

    @patch("commands.webbrowser.open")
    def test_youtube(self, mock_open):
        do_youtube()
        mock_open.assert_called_once_with("https://www.youtube.com")


class TestDoF5:
    """Тесты do_f5."""

    @patch("commands.ctypes.windll.user32.keybd_event")
    def test_f5(self, mock_keybd_event):
        do_f5()
        assert mock_keybd_event.call_count == 2


class TestFindPhpStorm:
    """Тесты find_phpstorm."""

    @patch("os.path.exists")
    def test_standard_path(self, mock_exists):
        mock_exists.return_value = True
        result = find_phpstorm()
        assert result is not None

    @patch("os.walk")
    @patch("os.path.exists")
    def test_not_found(self, mock_exists, mock_walk):
        mock_exists.return_value = False
        mock_walk.return_value = []
        result = find_phpstorm()
        assert result is None

    @patch("commands.sys.platform", "win32")
    @patch("os.path.exists")
    @patch("winreg.OpenKey")
    @patch("winreg.QueryValueEx")
    def test_registry(self, mock_query, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_query.return_value = (r"D:\Custom\PhpStorm", 1)

        result = find_phpstorm()

        assert result is not None
        assert "phpstorm" in result.lower()

    @patch("commands.get_all_drives")
    @patch("os.walk")
    @patch("os.path.exists")
    def test_all_drives_search(self, mock_exists, mock_walk, mock_drives):
        mock_exists.return_value = False
        mock_drives.return_value = ["C:\\", "D:\\", "E:\\"]
        mock_walk.return_value = [
            ("D:\\JetBrains/PhpStorm/bin", [], ["phpstorm64.exe"]),
        ]

        result = find_phpstorm()

        assert result is not None
        assert "D:" in result


class TestGetAllDrives:
    """Тесты get_all_drives."""

    @patch("commands.sys.platform", "win32")
    @patch("ctypes.windll.kernel32.GetLogicalDriveStringsA")
    @patch("ctypes.create_string_buffer")
    @patch("os.path.isdir")
    def test_windows_drives(self, mock_isdir, mock_buffer, mock_get_drives):
        mock_isdir.return_value = True
        mock_buffer.return_value.raw = b"C:\\\x00D:\\\x00\x00"
        mock_get_drives.return_value = 10

        drives = get_all_drives()
        assert "C:\\" in drives
        assert "D:\\" in drives

    @patch("commands.sys.platform", "linux")
    def test_linux_drives(self):
        drives = get_all_drives()
        assert drives == ["/"]


class TestActions:
    """Тесты словаря действий."""

    def test_actions_not_empty(self):
        assert len(ACTIONS) > 0

    def test_actions_have_exit(self):
        assert "exit" in ACTIONS

    def test_actions_have_alt_f2(self):
        assert "alt+f2" in ACTIONS

    def test_actions_have_dota(self):
        assert "steam://rungameid/570" in ACTIONS

    def test_actions_have_phpstorm(self):
        assert "phpstorm" in ACTIONS

    def test_actions_have_youtube(self):
        assert "https://www.youtube.com" in ACTIONS

    def test_actions_have_f5(self):
        assert "f5" in ACTIONS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
