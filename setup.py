# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
import sys
from setuptools import setup, find_packages
from version import get_version

name='gs.group.messages.add.smtp2gs'
version = get_version()

requires = ['setuptools',
            'lockfile',
            'gs.config',  # Note: without zope-support
            'gs.form', ]
if sys.version_info < (2, 7):
    # The argparse library was added to core in Python 2.7
    requires.append('argparse')
if sys.version_info < (3, 4):
    # Enum was added in Python 3.4
    requires.append('enum34')

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name=name,
    version=version,
    description="The console script for adding a message to GroupServer.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
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
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Mailing List Servers',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='groupserver, message, post, email, smtp, postfix',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/{0}'.format(name),
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['.'.join(name.split('.')[:i])
                        for i in range(1, len(name.split('.')))],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=['mock', ],
    test_suite="gs.group.messages.add.smtp2gs.tests.test_all",
    extras_require={'docs': ['Sphinx'], },
    entry_points={
        'console_scripts': [
            'smtp2gs = gs.group.messages.add.smtp2gs.script:main',
        ],
    },
)
