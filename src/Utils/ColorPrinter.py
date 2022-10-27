import sys

from IPython.display import Markdown

import colorama
from colorama import Fore
from colorama import Style

colorama.init()


class PrinterReplace:
    def __init__(self):
        self.first_line = True

    def colorprint(self, color, *args, end='\n'):
        # noinspection PyBroadException
        sys.stdout.write('\r')
        sys.stdout.write(color + Style.BRIGHT)
        sys.stdout.write(*args)
        sys.stdout.write(Style.RESET_ALL)

    def blueprint(self, *args, end='\n'):
        self.colorprint(Fore.BLUE, *args, end=end)

    def print(self, *args):
        if self.first_line:
            for arg in args:
                sys.stdout.write(arg)
            self.first_line = False
        else:
            sys.stdout.write('\r')
            for arg in args:
                sys.stdout.write(arg)

fore_to_html_color = {Fore.BLUE: "#00aaff",
                      Fore.RED: "#ff0000",
                      Fore.GREEN: "#00cc44"}

def colorprint(color, *args, end='\n'):
    # noinspection PyBroadException
    try:
        string = ""
        for arg in args:
            string += arg
        display(Markdown('<b><span style="color: ' + fore_to_html_color[color] + '">' + string + '</span></b>'))
    except Exception as e:
        print(color + Style.BRIGHT, end="")
        print(*args, end=end)
        print(Style.RESET_ALL, end="")


def blueprint(*args, end='\n'):
    colorprint(Fore.BLUE, *args, end=end)


def cyanprint(*args, end='\n'):
    colorprint(Fore.CYAN, *args, end=end)


def magentaprint(*args, end='\n'):
    colorprint(Fore.MAGENTA, *args, end=end)


def greenprint(*args, end='\n'):
    colorprint(Fore.GREEN, *args, end=end)


def yellowprint(*args, end='\n'):
    colorprint(Fore.YELLOW, *args, end=end)


def redprint(*args, end='\n'):
    colorprint(Fore.RED, *args, end=end)


if __name__ == "__main__":
    blueprint("hello", 42)
    redprint("hello", 32)