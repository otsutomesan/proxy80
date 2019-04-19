

from setuptools import setup
from uagent import __version__

setup(
  name='proxy80',
  version=__version__,
  description='proxy list',
  # author=__author__,
  packages=['proxy80'],
  install_requires=["requests"],
)

