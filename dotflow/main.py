"""Main"""

import argparse

from dotflow import __description__
from dotflow.cli.setup import Command


def main():
    """CLI DotFlow"""
    Command(
        parser=argparse.ArgumentParser(
            description=__description__
        )
    )


if __name__ == '__main__':
    main()
