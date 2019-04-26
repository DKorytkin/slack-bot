# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


here = os.path.realpath(os.path.dirname(__file__))


def parse_requirements(filename):
    """Read pip-formatted requirements from a file."""
    reqs = (line.strip() for line in open(filename))
    return [line for line in reqs if line and not line.startswith("#")]


def long_description():
    with open("README.md", "r") as fh:
        return fh.read()


install_requirements = parse_requirements(os.path.join(here, 'requirements.txt'))
tests_require = parse_requirements(os.path.join(here, 'requirements-dev.txt'))


setup(
    name="slack_bot",
    version='0.0.3',
    author='Denis Korytkin',
    author_email='dkorytkin@gmail.com',
    url='https://github.com/DKorytkin/slack-bot',
    description='Simple application for make slack bot',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    keywords=['bot', 'slack', 'app', 'slack_bot', 'app', 'application'],
    platforms=['linux'],
    packages=find_packages(exclude=['tests', 'tests.*', 'example']),
    py_modules=[
        'slack_bot.bot',
        'slack_bot.models',
        'slack_bot.routes',
    ],
    python_requires='>=3.6',
    install_requires=install_requirements,
    test_suite='tests',
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    license='MIT license',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
