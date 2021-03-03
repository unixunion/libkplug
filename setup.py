import os

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

try:
    from setuptools_scm import get_version
    version_git = get_version(root='.', relative_to=__file__)
    version_git = '.'.join(version_git.split('.')[:3])
    print("setting version from git: %s" % version_git)
except ImportError:
    with open(version_py, 'rt') as fh:
        version_git = "%s" % fh.read().strip().split('=')[-1].replace('"', '')
        print("setting version from file: %s" % version_git)

print("version: %s" % version_git)

setup(name='libkplug',
      version=version_git,
      description='Plugin Framework',
      author='Kegan Holtzhausen',
      author_email='marzubus@gmail.com',
      url='https://github.com/unixunion/libkplug/',
      package_dir={'': 'src'},
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
