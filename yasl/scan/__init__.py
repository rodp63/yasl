import click
import importlib

from yasl.scan.scanner import Scanner


def strip_code(code):
    counter = 0
    for c in code:
        if c.isspace():
            counter += 1
        else:
            break
    return "  " + code.strip(), counter - 1


def echo_error(error, filename, ending="\n"):
    line = "File {}, line {}, ".format(filename, error["line_number"])
    code, count = strip_code(error["line"])
    pointer = " " * (error["pointer"] - count) + "^"
    click.secho(line, bold=True, nl=False)
    click.secho("SyntaxError: ", nl=False, fg="red", bold=True)
    click.secho(error["message"], bold=True)
    click.echo("{}\n{}{}".format(code, pointer, ending))


@click.command(short_help="Scan a YASL file")
@click.argument("filename", type=click.Path(exists=True))
def yasl_command(filename):
    """Get the file tokens

    FILENAME is the file to scan.
    """

    scanner = Scanner()
    scanner.open_file(filename)

    tokens, errors = scanner.get_tokens()
    if errors:
        for error in errors[:-1]:
            echo_error(error, filename)
        echo_error(errors[-1], filename, "")
    else:
        for token in tokens:
            click.echo(token)
        click.secho("Ok! Scan completed", bold=True, fg="green")
