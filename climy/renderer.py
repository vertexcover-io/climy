from jinja2 import Environment, PackageLoader, select_autoescape

from climy.types import Command


def render_command(cmd: Command) -> str:
    env = Environment(loader=PackageLoader("climy"), autoescape=select_autoescape())
    tmpl = env.get_template("layout.html")
    return tmpl.render(cmd=cmd)
