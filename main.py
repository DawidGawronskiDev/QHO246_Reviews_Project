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
        self.branches: List[str] = []
        self.reviewers_locations: List[str] = []

        self.start()

    def start(self):
        TUI.print_title()
        self.reviews = Process.read_reviews('data/disneyland_reviews.csv')
        self.branches = Process.get_branches(self.reviews)
        self.reviewers_locations = Process.get_reviewers_locations(self.reviews)

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
            'B': lambda: self.b_submenu(),
            'X': lambda: exit()
        }

        while True:
            TUI.print_message(message)
            TUI.print_options(options, 1)
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
            'A': lambda: self.a_submenu_a(),
            'B': lambda: self.a_submenu_b(),
            'C': lambda: self.a_submenu_c(),
            'D': lambda: print(4)
        }

        while True:
            TUI.print_message(message)
            TUI.print_options(options, 2)
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

    def a_submenu_a(self):
        branch = TUI.validate_branch(
            'For which branch would you like to see reviews?',
            self.branches)
        TUI.print_reviews(Process.get_branch_reviews(branch, self.reviews))

    def a_submenu_b(self):
        branch = TUI.validate_branch(
            'For which reviewer location would you like to see number of reviews?',
            self.branches
        )

        location = TUI.validate_multi_choice(
            'For which reviewer location would you like to see number of reviews?',
            Process.get_reviewers_locations(self.reviews)
        )

        TUI.print_reviews_count(
            branch,
            location,
            Process.filter_reviews(self.reviews, {'branch': branch, 'reviewer_location': location})
        )

    def a_submenu_c(self):
        branch = TUI.validate_branch(
            'Select one of the following branches: ',
            self.branches
        )
        year = TUI.validate_multi_choice('Select one of the following years:',
                                         Process.get_reviews_years(branch, self.reviews))

        TUI.print_message(
            f'The average rating for {branch.replace('_', ' ')} branch in year {year} is {
            Process.get_avg_rating(
                Process.filter_reviews(self.reviews, {'branch': branch, 'year': year})
            )}')

    def b_submenu(self):
        message = 'Please enter one of the following options:'
        options = Process.create_options([
            'Most Reviewed Parks',
            'Average Scores',
            'Park Ranking by Nationality',
            'Most Popular Month by Park'
        ])

        actions = {
            'A': lambda: print(1),
            'B': lambda: print(2),
            'C': lambda: print(3),
            'D': lambda: print(4)
        }

        while True:
            TUI.print_message(message)
            TUI.print_options(options, 2)
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


if __name__ == '__main__':
    Controller()
