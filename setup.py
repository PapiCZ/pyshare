#!/usr/bin/env python

from distutils.core import setup
from pytransfer import __version__

try:
    import pytransfer
except (ImportError, SyntaxError):
    print("error: PyTransfer requires Python 3.6 or greater.")
    exit(1)

setup(
    name='PyTransfer',
    version=__version__,
    author='Patrik Janoušek',
    author_email='patrikjanousek97@gmail.com',
    description='App that simplifies usage of file hosting services (currently only https://transfer.sh)',
    install_requires=['argparse', 'tqdm', 'requests'],
    packages=['pytransfer'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': ['transfer=pytransfer.__main__:main']
    }
)
