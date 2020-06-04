# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['WelcomeScreen.py', 'gargn_earthworm\\src\\decomposer.py'],
             pathex=['C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src'],
             binaries=[],
             datas=[('C:\\\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'PyQt5\\Qt\\bin'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\button_exit.png', 'img\\button_exit.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\button_help.png', 'img\\button_help.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\button_open.png', 'img\\button_open.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\earthworm.png', 'img\\earthworm.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\icon_open.png', 'img\\icon_open.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\icon_saveas.png', 'img\\icon_saveas.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\icon_analyze.png', 'img\\icon_analyze.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\icon_fix.png', 'img\\icon_fix.png'),
             		('C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\img\\icon_selectall.png', 'img\\icon_selectall.png')],
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
          name='Earthworm',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\Tamari\\Dropbox\\Earthworm\\trunk\\src\\earthworm.ico')
