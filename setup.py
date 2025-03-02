#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotflow import __version__, __description__
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
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
        'Homepage': 'https://github.com/dotflow-io/dotflow',
        'Repository': 'https://github.com/dotflow-io/dotflow',
        'Documentation': 'https://dotflow-io.github.io/dotflow',
        'Issues': 'https://github.com/dotflow-io/dotflow/issues',
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=['dotflow'],
    include_package_data=True,
    python_requires=">=3.9",
    zip_safe=True,
    entry_points={
        'console_scripts': ['dotflow=dotflow.main:main'],
    },
)
