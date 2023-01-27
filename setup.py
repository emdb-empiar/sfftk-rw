# -*- coding: utf-8 -*-
# setup.py
import sys

from setuptools import setup, find_packages

from sfftkrw.conf import SFFTKRW_VERSION, SFFTKRW_ENTRY_POINT

with open(u'README.rst') as f:
    long_description = f.read()

SFFTKRW_NAME = u"sfftk-rw"
SFFTKRW_AUTHOR = u"Paul K. Korir, PhD"
SFFTKRW_AUTHOR_EMAIL = u"pkorir@ebi.ac.uk, paul.korir@gmail.com"
SFFTKRW_DESCRIPTION = u"Toolkit for reading and writing EMDB-SFF files"
SFFTKRW_DESCRIPTION_CONTENT_TYPE = u'text/x-rst; charset=UTF-8'
SFFTKRW_URL = u"http://sfftk-rw.readthedocs.io/en/latest/index.html"
SFFTKRW_LICENSE = u"Apache License 2.0"
SFFTKRW_KEYWORDS = [u"EMDB-SFF", u"SFF", u"segmentation"]
SFFTKRW_INSTALL_REQUIRES = ['six', 'numpy', "lxml", 'h5py', 'RandomWords']
SFFTKRW_CLASSIFIERS = [
    # maturity
    u"Development Status :: 4 - Beta",
    # environment
    u"Environment :: Console",
    u"Intended Audience :: Developers",
    u"Intended Audience :: Science/Research",
    # license
    u"License :: OSI Approved :: Apache Software License",
    # os
    u"Operating System :: OS Independent",
    # python versions
    u"Programming Language :: Python :: 3",
    u"Programming Language :: Python :: 3.6",
    u"Programming Language :: Python :: 3.7",
    u"Programming Language :: Python :: 3.8",
    u"Programming Language :: Python :: 3.9",
    u"Programming Language :: Python :: 3.10",
    u"Programming Language :: Python :: 3.11",
    u"Topic :: Software Development :: Libraries :: Python Modules",
    u"Topic :: Terminals",
    u"Topic :: Text Processing",
    u"Topic :: Text Processing :: Markup",
    u"Topic :: Utilities",
]
setup(
    name=SFFTKRW_NAME,
    version=SFFTKRW_VERSION,
    packages=find_packages(),
    author=SFFTKRW_AUTHOR,
    author_email=SFFTKRW_AUTHOR_EMAIL,
    description=SFFTKRW_DESCRIPTION,
    long_description=long_description,
    long_description_content_type=SFFTKRW_DESCRIPTION_CONTENT_TYPE,
    url=SFFTKRW_URL,
    license=SFFTKRW_LICENSE,
    keywords=SFFTKRW_KEYWORDS,
    install_requires=SFFTKRW_INSTALL_REQUIRES,
    classifiers=SFFTKRW_CLASSIFIERS,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            '{} = sfftkrw.sffrw:main'.format(SFFTKRW_ENTRY_POINT),
        ]
    },
)
