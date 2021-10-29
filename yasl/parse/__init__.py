import click
import importlib

from anytree import RenderTree
from anytree.exporter import DotExporter
from yasl.scan import scan_file
from yasl.parse.parser import Parser
from yasl.parse.grammar import yasl_grammar


def parse_file(filename):
    tokens = scan_file(filename, False)
    if not tokens:
        return

    parser = Parser(yasl_grammar)
    ok, tree, errors = parser.parse_tokens(tokens)
    if ok:
        click.echo("All good mai friends")
    else:
        for error in errors:
            click.echo(error)

    for pre, fill, node in RenderTree(tree):
        print(f"{pre}{node.name}")

    DotExporter(tree).to_picture("tree.png")


@click.command(short_help="Parse a YASL file")
@click.argument("filename", type=click.Path(exists=True))
def yasl_command(filename):
    """Parse a YASL file

    FILENAME is the file to parse.
    """

    return parse_file(filename)
