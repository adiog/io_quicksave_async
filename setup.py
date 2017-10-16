"""quicksave async

This file is a part of quicksave project.
Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

see: https://quicksave.io
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='quicksave async',

    version='0.0.0',

    description='quicksave async engine with plugins',
    long_description=long_description,

    url='https://github.com/adiog/io_quicksave_async',

    author='Aleksander Gajewski',
    author_email='adiog@quicksave.io',

    license='GPLv3',

    classifiers=[
        'Development Status:: 1 - Planning',

        'Environment :: Console',
        'Environment :: Plugins',

        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',

        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],

    keywords='quicksave async engine plugin',

    packages=find_packages('src'),

    install_requires=['pillow', 'selenium', 'pika', 'python-magic', 'beautifulsoup4', 'requests'],

    package_dir={
        '': 'src'
    },

    include_package_data=True,

    package_data={
    },

    entry_points={
        'console_scripts': [
            'qs-async=quicksave_async.pyasync:main',
        ],
    },
)
