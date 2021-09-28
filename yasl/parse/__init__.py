import click
import importlib

from yasl.scan import scan_file
from yasl.parse.parser import Parser


def parse_file(filename):
    tokens = scan_file(filename, False)
    if not tokens:
        return

    parser = Parser()
    parser.parse_tokens(tokens)


@click.command(short_help="Parse a YASL file")
@click.argument("filename", type=click.Path(exists=True))
def yasl_command(filename):
    """Parse a YASL file

    FILENAME is the file to parse.
    """

    return parse_file(filename)
