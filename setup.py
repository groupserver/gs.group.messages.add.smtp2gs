# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import codecs
import os
import sys
from setuptools import setup, find_packages
from version import get_version

version = get_version()

# The argparse library was added to core in Python 2.7
core = ['setuptools',
        'lockfile',
        'gs.config',  # Note: without zope-support
        'gs.form', ]
if sys.version_info > (2, 6):
    requires = core
else:
    requires = core + ['argparse']

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='gs.group.messages.add.smtp2gs',
    version=version,
    description="The console script for adding a message to GroupServer.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='groupserver message post topic images',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='http://groupserver.org/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group', 'gs.group.messages',
                        'gs.group.messages.add'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=['mock', ],
    test_suite="gs.group.messages.add.smtp2gs.test.test_all",
    extras_require={'docs': ['Sphinx'], },
    entry_points={
        'console_scripts': [
            'smtp2gs = gs.group.messages.add.smtp2gs.script:main',
            ],
        # --=mpj17=-- Entry points are the work of the devil. Some time
        # you, me and Mr Soldering Iron are going to have a little chat
        # about how to do things better.
        },
)
