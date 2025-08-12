# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for Academic Apex Strategist
Creates a standalone Windows executable with all dependencies
"""

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = os.path.abspath('.')

# Define data files to include
datas = [
    # Include all template files
    ('templates', 'templates'),
    # Include the agent configuration
    ('agent.yml', '.'),
    # Include the README for reference
    ('README.md', '.'),
    ('QUICK_START.md', '.'),
    ('START_HERE.md', '.'),
]

# Define hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    # Core Flask and web dependencies
    'flask',
    'werkzeug',
    'werkzeug.serving',
    'jinja2',
    'jinja2.ext',
    'requests',
    'urllib3',
    'ssl',
    'socket',
    'http.client',
    'email',
    'encodings.idna',
    'pkg_resources.py2_warn',
    
    # Core Python modules
    'pathlib',
    'json',
    'logging',
    'threading',
    'datetime',
    'typing',
    'os',
    'sys',
    'time',
    'signal',
    'subprocess',
    'io',
    'base64',
    'hashlib',
    'uuid',
    
    # Our custom modules
    'web_ui',
    'curator_service',
    'ollama_adapter',
    'obsidian_adapter',
    'slider_theme_controller',
    
    # Additional Flask extensions
    'flask.json',
    'flask.helpers',
    'werkzeug.utils',
    'werkzeug.exceptions',
    'werkzeug.wrappers',
    'werkzeug.routing',
    'werkzeug.security',
    
    # HTTP and networking
    'requests.adapters',
    'requests.auth',
    'requests.cookies',
    'requests.exceptions',
    'requests.models',
    'requests.sessions',
    'requests.utils',
    'urllib',
    'urllib.parse',
    'urllib.request',
    'urllib.error',
    'urllib3.util',
    'urllib3.poolmanager',
    'urllib3.exceptions',
    
    # Encoding and serialization
    'json.encoder',
    'json.decoder',
    'encodings',
    'encodings.utf_8',
    'encodings.ascii',
    'codecs',
    
    # File operations
    'shutil',
    'glob',
    'fnmatch',
    'tempfile',
    
    # Data structures
    'collections',
    'collections.abc',
    'itertools',
    'functools',
    'operator'
]

# Analysis configuration
a = Analysis(
    ['main_launcher.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'jupyter',
        'notebook'
    ],
    noarchive=False,
    optimize=0,
)

# Create PYZ archive
pyz = PYZ(a.pure)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AcademicApexStrategist',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window for startup messages and logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
    version_file=None,  # Add version info file if needed
)

# Optional: Create a one-folder distribution (uncomment if preferred)
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='AcademicApexStrategist'
# )
