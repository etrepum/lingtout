#!/usr/bin/env python

from setuptools import setup
#from distutils.core import setup

VERSION = '0.1'
DESCRIPTION = "Scrapes your vocabulary lists from lingt.com" 
LONG_DESCRIPTION = """
lingtout is a simple module that uses html5lib and simplejson to scrape
vocabulary lists from your lingt account.

"""

CLASSIFIERS = filter(None, map(str.strip,
"""                 
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))


setup(
    name="lingtout",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    author="Bob Ippolito",
    author_email="bob@redivi.com",
    url="http://github.com/etrepum/lingtout/tree/master",
    license="MIT License",
    py_modules=['lingtout'],
    platforms=['any'],
    install_requires=['html5lib', 'simplejson'],
)
