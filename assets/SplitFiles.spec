# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\src\\GUI.py', '..\\src\\SplitFiles.py', '..\\src\\model\\FileSignalData.py', '..\\src\\ui\\DragRectWidget.py', '..\\src\\ui\\FileItemWidget.py', '..\\src\\ui\\FileListWidget.py', '..\\src\\ui\\ProgressBarWidget.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5','PyQt5.QtCore','PyQt5.sip'],
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
    name='SplitFiles',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='my.txt',
    icon=['logo.ico'],
)
