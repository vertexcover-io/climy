from climy.parser import SupportedCommand, parse_command


def create_user_interface(sup_cmd: SupportedCommand) -> None:
    cmd = parse_command(sup_cmd)
    print(cmd)
