"""
TUI is short for Text-User Interface. This module is responsible for communicating with the user.
The functions in this module will display information to the user and/or retrieve a response from the user.
Each function in this module should utilise any parameters and perform user input/output.
A function may also need to format and/or structure a response e.g. return a list, tuple, etc.
Any errors or invalid inputs should be handled appropriately.
Please note that you do not need to read the data file or perform any other such processing in this module.
"""

from typing import Dict


class TUI:
    def __init__(self):
        pass

    @staticmethod
    def print_title() -> None:
        title = 'Disneyland Reviews Analyser'
        line = '*' * len(title)
        print(f'{line}\n{title}\n{line}')

    @staticmethod
    def print_options(options: Dict[str, str], indent: int = 0) -> None:
        if indent < 0:
            raise ValueError('Indent value must be greater than 0!')
        for k, v in options.items():
            print(f'{'\t' * indent}[{k}] {v}')

    @staticmethod
    def print_main_menu(options: Dict[str, str], indent: int = 0) -> None:
        message = 'Please enter the letter which corresponds with your desired menu choice:'
        print(message)
        TUI.print_options(options, indent)

    @staticmethod
    def handle_input():
        i = str(input()).strip()

        if len(i) == 0:
            print("Input cannot be empty!", end=' ')
            return
        else:
            return i
