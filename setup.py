#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup, find_packages

setup(
    name = 'PyZen',
    version = '0.3',
    packages = find_packages(),
    package_data = {'pyzen.ui': ['img/*']},
    author = 'Noah Kantrowitz',
    author_email = 'noah@coderanger.net',
    description = 'Continuous testing for paranoid developers.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license = 'BSD',
    keywords = 'test unittest continuous django',
    url = 'http://github.com/coderanger/pyzen',
    classifiers = [
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe = False,
    entry_points = {
        'distutils.commands': [
            'zen = pyzen.distutils:zen',
        ],
        'console_scripts': [
            'pyzen = pyzen.simple:main',
        ],
    },
)
