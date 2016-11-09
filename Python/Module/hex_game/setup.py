from distutils.core import setup

setup(name='hex_game',
      version='1.0',
      description='Hex in Python',
      packages=['hex_game'],
      requires=['numpy', 'Pillow', 'pyscreenshot']
      )
