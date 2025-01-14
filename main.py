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
        message = 'Please enter the letter which corresponds with your desired menu choice:'
        options = Process.create_options([
            'View Data',
            'Visualise Data'
        ])
        options['X'] = 'Exit'

        actions = {
            'A': lambda: self.a_submenu(),
            'B': lambda: print(2),
            'X': lambda: exit()
        }

        while True:
            TUI.print_menu(message, options, 1)
            choice = TUI.handle_input()

            if choice:
                choice = choice.upper()
                if choice in actions:
                    TUI.print_confirmed_option((choice, options[choice]))
                    actions[choice]()
                    if choice in ['A', 'B']:
                        break
                else:
                    print('Input does not correspond with any option!', end=' ')

    def a_submenu(self):
        message = 'Please enter one of the following options:'
        options = Process.create_options([
            'View Reviews by Park',
            'Number of Reviews by Park and Reviewer Location',
            'Average Score per year by Park',
            'Average Score per Park by Reviewer Location'
        ])

        actions = {
            'A': lambda: print(1),
            'B': lambda: print(2),
            'C': lambda: print(3),
            'D': lambda: print(4)
        }

        while True:
            TUI.print_menu(message, options, 2)
            choice = TUI.handle_input()

            if choice:
                choice = choice.upper()
                if choice in actions:
                    TUI.print_confirmed_option((choice, options[choice]))
                    actions[choice]()
                    if choice in options.keys():
                        break
                else:
                    print('Input does not correspond with any option!', end=' ')

    def b_submenu(self):
        pass


if __name__ == '__main__':
    Controller()
