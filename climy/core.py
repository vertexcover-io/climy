from climy.parser import SupportedCommand, parse_command
from climy.renderer import render_command


def create_user_interface(sup_cmd: SupportedCommand) -> str:
    cmd = parse_command(sup_cmd)
    print(cmd)
    return render_command(cmd)
