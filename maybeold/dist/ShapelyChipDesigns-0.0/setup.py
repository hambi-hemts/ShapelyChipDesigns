
from distutils.core import setup

setup(name = 'ShapelyChipDesigns',
      version = '0.0',
      description = 'Chip design package based on the Shapely module', 
      author = 'hambi',
      author_email = 'annahambi@gmail.com',
      url = 'lala.com',
      #py_modules=['src'],
      packages = ['ShapelyChipDesigns'], 
      package_dir = {'': 'src'},
      package_data = {'': ['convert.rb']},
      install_requires=[
            'shapely',
            'descartes', 
            'mpld3']
      #data_files=[('', ['ShapelyChipDesigns/convert.rb'])]
      )

"""
setup(name='ShapelyChipDesigns',
      version='0.0',
      description='Chip design package based on the Shapely module', 
      author='hambi',
      author_email='annahambi@gmail.com',
      url='lala.com',
      #py_modules=['src'],
      packages=['ShapelyChipDesigns'], 
      package_dir = {'ShapelyChipDesigns': 'src'},
      package_data={'ShapelyChipDesigns': ['convert.rb']}
      #data_files=[('', ['ShapelyChipDesigns/convert.rb'])]
      )"""