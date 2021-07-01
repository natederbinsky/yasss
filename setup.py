#!/usr/bin/env python

from distutils.core import setup

setup(name='yasss',
      version='0.1',
      description='Yet Another Static Site System',
      author='Nate Derbinsky',
      author_email='nate.derbinsky@gmail.com',
      url='https://derbinsky.info',
      packages=['yasss'],
      install_requires=['Jinja2', 'jinja2-highlight', 'MarkupSafe', 'Pygments', 'typing_extensions'],
     )
