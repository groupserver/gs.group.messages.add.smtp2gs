# -*- coding: utf-8 -*-
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

setup(name='gs.group.messages.add.smtp2gs',
    version=version,
    description="The console script for adding a message to GroupServer.",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
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
    zip_safe=True,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'smtp2gs = gs.group.messages.add.smtp2gs.script:main',
            ],
        # --=mpj17=-- Entry points are the work of the devil. Some time
        # you, me and Mr Soldering Iron are going to have a little chat
        # about how to do things better.
        },
)
