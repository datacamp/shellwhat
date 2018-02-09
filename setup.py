#!/usr/bin/env python

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('shellwhat/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
	name='shellwhat',
	version=version,
	packages=['shellwhat'],
	install_requires=['protowhat>=0.5.0'],
        description = 'Submission correctness tests for shell languages',
        author = 'Michael Chow',
        author_email = 'michael@datacamp.com',
        url = 'https://github.com/datacamp/shellwhat')
