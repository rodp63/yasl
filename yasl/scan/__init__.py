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
    line = "File {}, line {}, ".format(
        click.format_filename(filename), error["line_number"]
    )
    code, count = strip_code(error["line"])
    pointer = " " * (error["pointer"] - count) + "^"
    click.secho(line, bold=True, nl=False, err=True)
    click.secho("SyntaxError: ", nl=False, fg="red", bold=True, err=True)
    click.secho(error["message"], bold=True, err=True)
    click.echo("{}\n{}{}".format(code, pointer, ending), err=True)


def scan_file(filename, output):
    scanner = Scanner()
    scanner.open_file(filename)

    tokens, errors = scanner.get_tokens()
    if errors:
        for error in errors[:-1]:
            echo_error(error, filename)
        echo_error(errors[-1], filename, "")
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
