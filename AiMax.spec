# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('font', 'font'),          # کل پوشه font/
        ('logo.png', '.'),         # لوگو
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AiMax',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                # ← پنجره CMD باز نشه
    icon='logo.ico' if os.path.isfile('logo.ico') else None,
)