#!/usr/bin/env python

import argparse

from dotflow.cli.setup import Command


def main():
    Command(
        parser=argparse.ArgumentParser(
            description='🎲 Dotflow turns an idea into flow quickly!'
        )
    )


if __name__ == '__main__':
    main()
