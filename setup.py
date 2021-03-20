import os

from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

with open(version_py, 'rt') as fh:
    version = "%s" % fh.read().strip().split('=')[-1].replace('"', '').strip()
    print("setting version from file: %s" % version)

print("version: %s" % version)

setup(name='libkplug',
      version=version,
      description='Plugin Framework',
      author='Kegan Holtzhausen',
      author_email='marzubus@gmail.com',
      url='https://github.com/unixunion/libkplug/',
      package_dir={'': 'src'},
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=[
          'PyYAML>=3.11'
      ],
      packages=[
          'libkplug',
          'libksettings'
      ],
      use_scm_version=False,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      tests_require=[
          'nose2==0.10.0',
          'unittest2==1.1.0'
      ]
      )
