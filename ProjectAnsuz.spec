# -*- mode: python ; coding: utf-8 -*-
# ProjectAnsuz.spec  — single-file Windows EXE
# Usage:  pyinstaller ProjectAnsuz.spec

block_cipher = None

a = Analysis(
    ['ansuz.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # edge-tts & async
        'edge_tts',
        'edge_tts.communicate',
        'edge_tts.list_voices',
        'asyncio',
        'asyncio.events',
        'asyncio.base_events',
        'aiohttp',
        'aiohttp.client',
        'certifi',
        # audio playback
        'pygame',
        'pygame.mixer',
        # mic / speech recognition
        'speech_recognition',
        'audioop',
        'pyaudio',
        # image / icon support
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.BmpImagePlugin',
        'PIL.PngImagePlugin',
        # stdlib used at runtime
        'concurrent.futures',
        'tempfile',
        'base64',
        'tkinter',
        'tkinter.ttk',
        'tkinter.font',
        'tkinter.messagebox',
        # fallback TTS
        'pyttsx3',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'scipy', 'pandas',
        'IPython', 'jupyter', 'notebook',
        'PyQt5', 'PyQt6', 'wx',
    ],
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
    name='ProjectAnsuz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,           # ← no black console window on launch
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rune_icon.ico',    # ← EXE file icon in Explorer/taskbar
    version_file=None,
)
