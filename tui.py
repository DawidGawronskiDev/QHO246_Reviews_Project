"""
TUI is short for Text-User Interface. This module is responsible for communicating with the user.
The functions in this module will display information to the user and/or retrieve a response from the user.
Each function in this module should utilise any parameters and perform user input/output.
A function may also need to format and/or structure a response e.g. return a list, tuple, etc.
Any errors or invalid inputs should be handled appropriately.
Please note that you do not need to read the data file or perform any other such processing in this module.
"""

from process import Process, Review
from typing import Dict, List, Tuple


class TUI:
    def __init__(self):
        pass

    @staticmethod
    def print_title() -> None:
        title = 'Disneyland Reviews Analyser'
        line = '*' * len(title)
        print(f'{line}\n{title}\n{line}')

    @staticmethod
    def print_options(options: Dict[str, str] | List[Tuple[str, str]], indent: int = 0) -> None:
        if indent < 0:
            raise ValueError('Indent value must be greater than 0!')

        if not isinstance(options, dict):
            for k, v in options:
                print(f'{'\t' * indent}{k} {v.replace('_', ' ')}')
        else:
            for k, v in options.items():
                print(f'{'\t' * indent}[{k}] {v.replace('_', ' ')}')

    @staticmethod
    def print_message(message: str) -> None:
        print(message)

    @staticmethod
    def handle_input():
        i = str(input()).strip()

        if len(i) == 0:
            print("Input cannot be empty!", end=' ')
            return
        else:
            return i

    @staticmethod
    def print_confirmed_option(option: Tuple[str] | str):
        if isinstance(option, str):
            print(f'You have chosen option - {option}')
        else:
            print(f'You have chosen option {option[0]} - {option[1]}')

    @staticmethod
    def print_reviews(reviews: List[Review]) -> None:
        for review in reviews:
            print(review)

    @staticmethod
    def print_reviews_count(branch: str, loc: str, reviews: List[Review]) -> None:
        print(f'There are {len(reviews)} reviews from reviewers from {loc} for {branch} branch.')

    @staticmethod
    def validate_branch(msg: str, branches: List[str]) -> str:
        branch_options = Process.create_options(branches)

        while True:
            TUI.print_message(msg)
            TUI.print_options(branch_options, 3)
            choice = TUI.handle_input()

            if choice:
                choice = choice.upper()
                if choice in branch_options:
                    choice = branch_options[choice]
                    break
                else:
                    print('Input does not correspond with any option!', end=' ')
        return choice
