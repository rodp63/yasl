import click
import importlib

from yasl.scan.scanner import Scanner


@click.command(short_help="Scan a YASL file")
@click.argument("filename", type=click.Path(exists=True))
def yasl_command(filename):
    """Get the file tokens

    FILENAME is the file to scan.
    """

    scanner = Scanner()
    scanner.open_file(filename)

    tokens = scanner.get_tokens()
    for token in tokens:
        click.echo(token)
