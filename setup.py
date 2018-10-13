#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

setup(name='gs',
      version='1.0',
      description='GraphShop Server',
      author=[
          "Austin Graham"
      ],
      author_email=[
          "austin.graham@ou.edu",
      ],
      url='https://github.com/austinpgraham/GraphShop',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      entry_points = {
          'console_scripts': [
          ]
      },
      install_requires=[
          'sqlalchemy',
          'pyhamcrest',
          'nose2'
      ]
    )
