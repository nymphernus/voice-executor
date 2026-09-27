# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Путь к проекту
project_root = Path(SPECPATH)

# Путь к DLL Vosk
vosk_path = Path(sys.executable).parent.parent / "Lib" / "site-packages" / "vosk"

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        (str(vosk_path / "*"), "vosk"),
    ],
    datas=[
        ('config.example.toml', '.'),
    ],
    hiddenimports=[
        'voice_assistant',
        'voice_assistant.app',
        'voice_assistant.config',
        'voice_assistant.logging_setup',
        'voice_assistant.audio',
        'voice_assistant.recognizer',
        'voice_assistant.nlu',
        'voice_assistant.executor',
        'voice_assistant.model_manager',
        'voice_assistant.commands',
        'voice_assistant.commands.system',
        'voice_assistant.commands.browser',
        'voice_assistant.commands.apps',
        'voice_assistant.commands.discord',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='voice-executor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
