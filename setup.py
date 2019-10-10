from distutils.core import setup
setup(
  name = 'lbox',
  py_modules = ['lbox'],
  version = '0.0.0.1',
  description = 'a very simple python wrapper for the label-box api',
  author = 'Brookie Guzder-Williams',
  author_email = 'brook.williams@gmail.com',
  url = 'https://github.com/brookisme/lbox',
  download_url = 'https://github.com/brookisme/lbox/tarball/0.1',
  keywords = ['labelbox','api m.jk'],
  include_package_data=True,
  data_files=[
    (
      'config',[]
    )
  ],
  classifiers = [],
  entry_points={
      'console_scripts': [
      ]
  }
)