#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotflow import __version__
from setuptools import setup
from setuptools.command.install import install


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CustomInstallCommand(install):
    def run(self):
        install.run(self)


setup(
    name="dotflow",
    fullname='dotflow',
    version=__version__,
    author="Fernando Celmer",
    author_email="email@fernandocelmer.com",
    description="DotFlow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
        'Homepage': 'https://github.com/linux-profile/dotflow',
        'Repository': 'https://github.com/linux-profile/dotflow',
        'Documentation': 'https://github.com/linux-profile/dotflow/blob/master/README.md',
        'Issues': 'https://github.com/linux-profile/dotflow/issues',
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3.0",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    packages=['dotflow'],
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=True,
    entry_points={
        'console_scripts': ['flow=dotflow.main:main'],
    },
)
