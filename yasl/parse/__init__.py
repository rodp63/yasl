import click

from copy import deepcopy
from anytree import RenderTree
from anytree.exporter import DotExporter
from yasl.parse.parser import Parser
from yasl.parse.grammar import yasl_grammar, epsilon, eof
from yasl.scan import scan_file
from yasl.utils import echo_error, path_of_tree_file


def _echo_error(error, filename, ending="\n"):
    if isinstance(error, str):
        click.secho("Compiler Error", bold=True, err=True, fg="red", nl=False)
        click.secho(": {}".format(error), bold=True, err=True)
    else:
        echo_error(error, filename, "SyntaxError", ending)


def parse_file(filename, output, image):
    tokens = scan_file(filename, False)
    if not tokens:
        return
    try:
        parser = Parser(yasl_grammar, epsilon, eof)
        tokens_copy = deepcopy(tokens)
        tree, errors = parser.parse_tokens(tokens)
        if errors:
            with open(filename, "r") as code:
                lines = code.read().split("\n")
                for error in errors:
                    error["line"] = lines[error["line_number"] - 1]

                for error in errors[:-1]:
                    _echo_error(error, filename)
                _echo_error(errors[-1], filename, "")
            return None
        else:
            if output:
                for pre, fill, node in RenderTree(tree):
                    print("{}{}".format(pre, node.name))
                click.secho("Ok! Parsing completed", bold=True, fg="green")
            if image:
                DotExporter(tree).to_picture(path_of_tree_file(filename))
            return tree, tokens_copy
    except Exception as ex:
        _echo_error(str(ex), filename)
        return None


@click.command(short_help="Parse a YASL file")
@click.argument("filename", type=click.Path(exists=True))
@click.option("-o", "--output", is_flag=True, help="Print the output of the parser")
@click.option("-i", "--image", is_flag=True, help="Save the parse tree in PNG format")
def yasl_command(filename, output, image):
    """Parse a YASL file

    FILENAME is the file to parse.
    """

    return parse_file(filename, output, image)
