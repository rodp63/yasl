import click
import importlib


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option("0.1")
def cli():
    pass


commands = [
    "scan",
    "parse",
]

for command in commands:
    module = importlib.import_module("yasl.{}".format(command))
    cli.add_command(module.yasl_command, command)
