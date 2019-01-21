import os
import subprocess
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

install_requires = [
    'pyyaml>=4.2b1'
]

# try:
#     import importlib
# except ImportError:
#     install_requires.append('importlib')

try:
    p = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o = p.communicate()
    if p.returncode != 0:
        raise Exception('git describe failed to execute reason: %s' % o[1])
    version_git = "%s" % o[0].rstrip().decode("utf-8")
    print("setting version from git")
except Exception as e:
    with open(version_py, 'rt') as fh:
        version_git = "%s" % fh.read().strip().split('=')[-1].replace('"', '')
        print("setting version from file")

print("version: %s" % version_git)

version_msg = "# Do not edit this file, versions governed by git tags"
with open(version_py, 'wt') as fh:
    fh.write("%s%s__version__=%s" % (version_msg, os.linesep, version_git))

setup(name='libkplug',
      version="{ver}".format(ver=version_git),
      description='Plugin Framework',
      author='Kegan Holtzhausen',
      author_email='marzubus@gmail.com',
      package_dir={'': 'src'},
      packages=[
          'libkplug',
          'libksettings'
      ],
      setup_requires=[

      ],
      tests_require=[
          'nose2==0.8.0',
          'unittest2==1.1.0'
      ],
      install_requires=install_requires,
      )
