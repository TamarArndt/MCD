#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('VERSION', 'r') as version_file:
    version = version_file.readline().strip()

with open('LICENSE', 'r') as license_file:
    licence = license_file.readline().strip()

with open('README.rst') as readme_file:
    readme = readme_file.read()


# Requirements
install_reqs = parse_requirements('requirements.txt', session='hack')
requirements = [str(ir.req) for ir in install_reqs]


test_requirements = []

classifiers = [
    'Natural Language :: English',
]


setup(
    name='mobility-companion-desktop',
    version=version,
    description='Desktop application for easy labeling of data collected by the mobility-companion-app',
    long_description=readme,
    author='Tamar Arndt',
    author_email='arndt.tamar@gmail.com',
    url='https://git.seedup.de/Tamar Arndt/mobility-companion-desktop',
    packages=['mc-desktop'],
    package_dir={'mobility-companion-desktop': 'mc-desktop'},
    install_requires=requirements,
    license=licence,
    keywords='mobility-companion-desktop',
    classifiers=classifiers,
    test_suite='tests',
    tests_require=test_requirements,
    scripts=['bin/mobility-companion-desktop'],
    # instead of scripts maybe use: entry_points={'console_scripts': ['mc-desktop=mc-desktop:main',],},
)
