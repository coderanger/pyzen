#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup

setup(
    name = 'PyZen',
    version = '0.1',
    packages = ['pyzen'],
    package_data = { 'pyzen': [] },

    author = 'Noah Kantrowitz',
    author_email = 'noah@coderanger.net',
    description = 'Continuous testing for paranoid developers.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license = 'BSD',
    keywords = 'test django continuous',
    url = 'http://github.com/coderanger/django-zen',
    classifiers = [
        'Framework :: Django',
        'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    
    install_requires = ['Django'],
)