#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# python setup.py build
# python setup.py sdist
# python setup.py bdist_egg
# LATEST

# python3 setup.py bdist_wheel --universal

# from __future__ import absolute_import
# from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='mongosafe',
    version='0.0.4',
    license='MIT license',
    description='Provides safe reference fields for mongoengine and Flask-admin dashboard.',
    author='Alexandre Bassel',
    author_email='abassel@gmail.com',
    url='https://github.com/abassel/mongosafe',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        # 'Topic :: Utilities',
    ],
    keywords=[
        'mongoengine', 'Flask-admin', 'flask',
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        'mongoengine>=0.15.0'
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    # extras_require={
    #     # eg:
    #     #   'rst': ['docutils>=0.11'],
    #     #   ':python_version=="2.6"': ['argparse'],
    # },
    # entry_points={
    #     'console_scripts': [
    #         'mongosafe = mongosafe.cli:main',
    #     ]
    # },
)
