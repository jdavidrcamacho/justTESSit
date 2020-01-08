#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='justtessit',
      version='0.1',
      description='Tiny script to see if a given star is going to be observed with TESS',
      author='João Camacho',
      author_email='joao.camacho@astro.up.pt',
      license='MIT',
      url='https://github.com/jdavidrcamacho/justTESSit',
      packages=['justtessit'],
      install_requires=[
        'numpy',
        'astropy',
        'tess-point'
      ],
     )
