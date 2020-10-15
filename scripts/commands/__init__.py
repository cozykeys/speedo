import argparse


def add_command_parsers(subparsers: argparse._SubParsersAction) -> None:
    from .scratch import add_scratch_parser

    add_scratch_parser(subparsers)
