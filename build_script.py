import os
import sys
from typing import List

def create_version_file() -> None:
    """Create a version file for the executable"""
    version_script = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Windows Update Control'),
        StringStruct(u'FileDescription', u'Windows Update Control Tool'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'win_update_control'),
        StringStruct(u'LegalCopyright', u''),
        StringStruct(u'OriginalFilename', u'WindowsUpdateControl.exe'),
        StringStruct(u'ProductName', u'Windows Update Control'),
        StringStruct(u'ProductVersion', u'1.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    with open('version_info.txt', 'w') as f:
        f.write(version_script)

def build_exe() -> None:
    """Build the executable using PyInstaller"""
    # Create version info file
    create_version_file()
    
    # PyInstaller command line arguments
    pyinstaller_args: List[str] = [
        'pyinstaller',
        '--clean',
        '--onefile',
        '--uac-admin',  # Request admin privileges
        '--version-file=version_info.txt',
        '--name=WindowsUpdateControl',
        '--noconsole',  # Hide console window
        'update_control.py'  # Your main script name
    ]
    
    # Execute PyInstaller
    os.system(' '.join(pyinstaller_args))
    
    # Clean up version file
    if os.path.exists('version_info.txt'):
        os.remove('version_info.txt')

if __name__ == '__main__':
    build_exe()
