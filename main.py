"""
This module is responsible for the overall program flow. It controls how the user interacts with the
program and how the program behaves. It uses the other modules to interact with the user, carry out
processing, and for visualising information.

Note:   any user input/output should be done in the module 'tui'
        any processing should be done in the module 'process'
        any visualisation should be done in the module 'visual'
"""

from typing import List
from process import Process, Review
from tui import TUI


class Controller:
    def __init__(self):
        self.reviews: List[Review] = []

        self.start()

    def start(self):
        TUI.print_title()
        self.reviews = Process.read_reviews('data/disneyland_reviews.csv')

        while True:
            self.main_menu()

    def main_menu(self):
        options = Process.create_options([
            'View Data',
            'Visualise Data'
        ])
        options['X'] = 'Exit'

        while True:
            TUI.print_main_menu(options, 1)
            choice = TUI.handle_input()

            if choice and choice.upper() in options:
                if choice == 'A':
                    print(1)
                    break
                if choice == 'B':
                    print(2)
                    break
                if choice == 'X':
                    exit()


if __name__ == '__main__':
    Controller()
