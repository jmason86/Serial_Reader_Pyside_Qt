# -*- mode: python -*-

block_cipher = None


a = Analysis(['serial_reader.py'],
             pathex=['/Users/jmason86/Dropbox/Development/Python/Serial_Reader_Pyside_Qt'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='serial_reader',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='serial_reader.app',
             icon=None,
             bundle_identifier=None)
