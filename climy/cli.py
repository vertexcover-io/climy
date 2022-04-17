import importlib
import sys

import click

from climy.core import create_user_interface


def show_error(msg):
    click.echo(click.style(msg, fg="red"))
    sys.exit(1)


@click.command()
@click.argument("click_app")
def main(click_app):
    try:
        module_name, cmd_name = click_app.rsplit(".", 1)
    except ValueError:
        show_error(
            "Unable to load click command. App name must be passed as `<module_name>.<command_name>`"
        )

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        show_error(f"Unable to load click command. Module {module_name} not found")

    try:
        click_cmd = getattr(module, cmd_name)
    except AttributeError:
        show_error(f"Unable to load click command. Command {cmd_name} not found")

    click.echo("Click Command Found")
    create_user_interface(click_cmd)
