"""Команды для запуска приложений."""

import logging
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

logger = logging.getLogger(__name__)


def do_dota() -> None:
    """Запускает Dota 2 через Steam."""
    logger.info("Запуск Dota 2")
    print("Запускаю Dota 2...")
    webbrowser.open("steam://rungameid/570")


def do_phpstorm() -> None:
    """Открывает PHPStorm."""
    logger.info("Запуск PHPStorm")
    print("Открываю PHPStorm...")

    path = _find_phpstorm()
    if path:
        try:
            subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"PHPStorm запущен: {path}")
        except Exception as e:
            logger.error(f"Ошибка запуска PHPStorm: {e}")
            print(f"Ошибка запуска: {e}")
    else:
        logger.warning("PHPStorm не найден")
        print("PHPStorm не найден на компьютере.")


def _find_phpstorm() -> str | None:
    """Ищет PHPStorm на всех дисках."""
    # 1. Стандартные пути
    program_files = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.environ.get("LocalAppData", ""),
    ]
    for pf in program_files:
        if not pf:
            continue
        for exe in ["phpstorm64.exe", "phpstorm.exe"]:
            path = os.path.join(pf, "JetBrains", "PhpStorm", "bin", exe)
            if os.path.exists(path):
                return path

    # 2. Реестр Windows
    if sys.platform == "win32":
        try:
            import winreg
            for hkey, subkey in [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\JetBrains\PhpStorm"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\JetBrains\PhpStorm"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\JetBrains\PhpStorm"),
            ]:
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
                        if install_path:
                            exe = os.path.join(install_path, "bin", "phpstorm64.exe")
                            if os.path.exists(exe):
                                return exe
                except OSError:
                    continue
        except Exception:
            pass

    # 3. Поиск по всем дискам
    logger.info("Поиск PHPStorm на всех дисках...")
    drives = _get_all_drives()
    skip_dirs = {
        "windows", "programdata", "$recycle.bin", "system volume information",
        "msocache", "recovery", "perflogs",
    }
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            dirs[:] = [d for d in dirs if d.lower() not in skip_dirs]
            for file in files:
                if file.lower() in ("phpstorm64.exe", "phpstorm.exe"):
                    return os.path.join(root, file)

    return None


def _get_all_drives() -> list[str]:
    """Возвращает список всех доступных дисков."""
    drives = []
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        buffer = ctypes.create_string_buffer(260)
        result = kernel32.GetLogicalDriveStringsA(260, buffer)
        if result:
            drive_strings = buffer.raw.decode("ascii").split("\x00")
            for d in drive_strings:
                if d and os.path.isdir(d):
                    drives.append(d)
    else:
        drives.append("/")
    return drives
