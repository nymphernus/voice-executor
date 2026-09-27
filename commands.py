"""
Команды голосового ассистента.
Каждая команда — функция, которая выполняет действие.
"""

import os
import sys
import subprocess
import webbrowser
import ctypes

# Виртуальные коды клавиш Windows
VK_MENU = 0x12   # Alt
VK_F2 = 0x71     # F2
VK_F5 = 0x74     # F5


def do_exit():
    """Завершение работы."""
    print("Завершение работы...")
    sys.exit(0)


def do_alt_f2():
    """Нажимает Alt+F2 (переключение микрофона в Discord)."""
    print("Переключаю микрофон в Discord (Alt+F2)...")
    try:
        user32 = ctypes.windll.user32
        # Нажимаем Alt
        user32.keybd_event(VK_MENU, 0, 0, 0)
        # Нажимаем F2
        user32.keybd_event(VK_F2, 0, 0, 0)
        # Отпускаем F2
        user32.keybd_event(VK_F2, 0, 2, 0)
        # Отпускаем Alt
        user32.keybd_event(VK_MENU, 0, 2, 0)
    except Exception as e:
        print(f"Ошибка: {e}")


def do_dota():
    """Запускает Dota 2."""
    print("Запускаю Dota 2...")
    webbrowser.open("steam://rungameid/570")


def do_phpstorm():
    """Открывает PHPStorm."""
    print("Открываю PHPStorm...")
    import subprocess
    import os

    path = find_phpstorm()
    if path:
        try:
            subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Ошибка запуска: {e}")
    else:
        print("PHPStorm не найден на компьютере.")


def find_phpstorm():
    """Ищет PHPStorm на всех дисках."""
    import os
    import subprocess

    # 1. Быстрая проверка стандартных путей
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
    print("Поиск PHPStorm на всех дисках...")
    drives = get_all_drives()
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


def get_all_drives():
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


def do_youtube():
    """Открывает YouTube."""
    print("Открываю YouTube...")
    webbrowser.open("https://www.youtube.com")


def do_f5():
    """Нажимает F5 (обновление страницы)."""
    print("Обновляю страницу (F5)...")
    try:
        user32 = ctypes.windll.user32
        user32.keybd_event(VK_F5, 0, 0, 0)
        user32.keybd_event(VK_F5, 0, 2, 0)
    except Exception as e:
        print(f"Ошибка: {e}")


# Маппинг действий к функциям
ACTIONS = {
    "exit": do_exit,
    "alt+f2": do_alt_f2,
    "steam://rungameid/570": do_dota,
    "phpstorm": do_phpstorm,
    "https://www.youtube.com": do_youtube,
    "f5": do_f5,
}
