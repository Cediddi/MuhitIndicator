#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Humbly cloned from captn3m0's HackerTray package. What a wonderful app he wrote."""

from setuptools import setup
from setuptools import find_packages

setup(name='muhit_indicator,',
      version='2.0.0',
      description='Muhit.geekyapar.com most recent post indicator.',
      long_description='This indicator fetches most recently updated threads from Muhit.geekyapar.com.',
      keywords='Geekyapar\'s Muhit system tray indicator unity',
      url='http://muhit.geekyapar.com/',
      author='Umut Karcı',
      author_email='umutkarci@std.sehir.edu.tr',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests>=2.5.3',
          'appdirs>=1.3.0',
      ],
      entry_points={
          'console_scripts': ['muhit_indicator=muhit_indicator:main'],
          },
      zip_safe=False)