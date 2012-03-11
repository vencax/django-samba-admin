#!/usr/bin/env python
from setuptools import setup, find_packages
import os

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README')

description = 'Login script generator for windoze samba users stored in SQL DB.'

if os.path.exists(README_PATH):
    long_description = open(README_PATH).read()
else:
    long_description = description

setup(name='django-samba-admin',
    version='0.1',
    description=description,
    license='BSD',
    url='https://github.com/vencax/django-samba-admin',
    author='vencax',
    author_email='vencax@centrum.cz',
    packages=find_packages(),
    install_requires=[
        'django>=1.3',
    ],
    keywords="django linux samba admin",
    include_package_data=True,
)
