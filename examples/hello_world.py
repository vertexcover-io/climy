import time

import click


@click.command()
@click.argument("msg_list", nargs=-1)
@click.option("-s", "--sleep", type=click.FLOAT, default=0.5)
def hello(msg_list: list[str], sleep: float):
    """
    Print Hello Message
    """
    print("Hello\n")
    for m in msg_list:
        time.sleep(sleep)
        print(m)


if __name__ == "__main__":
    print("Run Main")
    hello()
