# -*- mode: python -*-
import os

block_cipher = None

filelist= [(os.path.join('src','images',file), "src\images") for file in os.listdir(os.path.join('src','images')) if file.endswith('.png')]

a = Analysis(['src\\sql_editor.py'],
             pathex=['c:\\1\\sql_editor'],
             binaries=[],
             datas=filelist,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='sql_editor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\1\\sql_editor\\src\\images\\Opal_database.ico')
