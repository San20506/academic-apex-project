# -*- mode: python ; coding: utf-8 -*-
# Academic Apex Theme Overlay - PyInstaller Specification File

import sys
from pathlib import Path

# Define paths
project_root = Path.cwd()
main_script = project_root / "theme_overlay.py"

block_cipher = None

a = Analysis(
    [str(main_script)],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / "apply-cmd-theme.ps1"), "."),
        (str(project_root / "README-Overlay.md"), "."),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.colorchooser',
        'json',
        'subprocess',
        'threading',
        'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'PIL',
        'scipy',
        'pandas',
        'flask',
        'requests',
        'urllib3',
        'werkzeug',
        'jinja2'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary modules to reduce file size
a.binaries = [x for x in a.binaries if not any(exclude in x[0].lower() for exclude in [
    'api-ms-win', 'ucrtbase', '_ssl', '_hashlib', '_bz2', '_lzma', 'select'
])]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AcademicApexThemeOverlay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
    version_file=None,  # Add version file here if you want
)

# Additional options for Windows
if sys.platform.startswith('win'):
    exe.manifest = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="AcademicApexThemeOverlay" type="win32"/>
    <description>Academic Apex Theme Overlay</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="*" publicKeyToken="6595b64144ccf1df" language="*"/>
        </dependentAssembly>
    </dependency>
    <application xmlns="urn:schemas-microsoft-com:asm.v3">
        <windowsSettings>
            <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
            <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
        </windowsSettings>
    </application>
</assembly>"""
