import click

from yasl.scan.scanner import Scanner
from yasl.utils import echo_error


def scan_file(filename, output):
    scanner = Scanner()
    scanner.open_file(filename)

    tokens, errors = scanner.get_tokens()
    if errors:
        for error in errors[:-1]:
            echo_error(error, filename, "LexicalError")
        echo_error(errors[-1], filename, "LexicalError", "")
        return None
    else:
        if output:
            for token in tokens:
                click.echo(token)
            click.secho("Ok! Scan completed", bold=True, fg="green")
        return tokens


@click.command(short_help="Scan a YASL file")
@click.argument("filename", type=click.Path(exists=True))
@click.option("-o", "--output", is_flag=True, help="Print the output of the scanner")
def yasl_command(filename, output):
    """Get the file tokens

    FILENAME is the file to scan.
    """

    return scan_file(filename, output)
