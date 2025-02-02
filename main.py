"""
This module is responsible for the overall program flow. It controls how the user interacts with the
program and how the program behaves. It uses the other modules to interact with the user, carry out
processing, and for visualising information.

Note:   any user input/output should be done in the module 'tui'
        any processing should be done in the module 'process'
        any visualisation should be done in the module 'visual'
"""

from typing import Dict, List
from exporter import Review, Branch
from process import Process
from visual import Visual
from tui import TUI


class Controller:
    def __init__(self):
        self.reviews: List[Review] = []
        self.branches: Dict[str, Branch] = {}
        self.reviewers_locations: List[str] = []

        self.start()

    def start(self):
        TUI.print_title()
        self.branches = Process.read_reviews('data/disneyland_reviews.csv')
        print(f'There are {Process.count_reviews(self.branches)} reviews.')
        while True:
            self.main_menu()

    def main_menu(self):
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
            TUI.print_message('Please enter the letter which corresponds with your desired menu choice:')
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
                    print('Input does not correspond with any option!')

    def a_submenu(self):
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
            'D': lambda: self.a_submenu_d()
        }

        while True:
            TUI.print_message('Please enter one of the following options:')
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
                    print('Input does not correspond with any option!')

    def a_submenu_a(self):
        branch = TUI.validate_branch(
            'For which branch would you like to see reviews?',
            list(self.branches.keys()))
        TUI.print_reviews(self.branches[branch].reviews)

    def a_submenu_b(self):
        branch = TUI.validate_branch(
            'For which reviewer location would you like to see number of reviews?',
            list(self.branches.keys())
        )

        location = TUI.validate_multi_choice(
            'For which reviewer location would you like to see number of reviews?',
            self.branches[branch].get_locations()
        )

        TUI.print_reviews_count(
            branch,
            location,
            Process.filter_reviews(self.branches[branch].get_reviews(),
                                   {'branch': branch, 'reviewer_location': location})
        )

    def a_submenu_c(self):
        branch = TUI.validate_branch(
            'Select one of the following branches: ',
            list(self.branches.keys())
        )
        year = TUI.validate_multi_choice('Select one of the following years:',
                                         self.branches[branch].get_reviews_years())

        TUI.print_message(
            f'The average rating for {self.branches[branch].get_name()} branch in year {year} is {
            self.branches[branch].get_avg_rating()}')

    def a_submenu_d(self):
        TUI.print_avg_score_by_loc(self.branches)

    def b_submenu_a(self):
        data = Process.get_branches_reviews_count(self.branches)
        reviews_count = list(data.values())
        Visual.show_chart("pie", 'Most Reviewed Parks', labels=reviews_count, vals=reviews_count,
                          legend=[self.branches[branch].get_name() for branch in list(data.keys())])

    def b_submenu_b(self):
        data = Process.get_avg_branches_rating(self.branches)
        Visual.show_chart("bar", 'Average Scores',
                          labels=[self.branches[branch].get_name() for branch in list(data.keys())],
                          vals=list(data.values()))

    def b_submenu_c(self):
        branch = TUI.validate_branch('Please enter one of the following options:', self.branches)
        data = self.branches[branch].get_top_locations(10)

        Visual.show_chart("bar", 'Park Ranking by Nationality', labels=[item[0] for item in data],
                          vals=[item[1] for item in data])

    def b_submenu(self):
        options = Process.create_options([
            'Most Reviewed Parks',
            'Average Scores',
            'Park Ranking by Nationality',
            'Most Popular Month by Park'
        ])

        actions = {
            'A': lambda: self.b_submenu_a(),
            'B': lambda: self.b_submenu_b(),
            'C': lambda: self.b_submenu_c(),
            'D': lambda: print(4)
        }

        while True:
            TUI.print_message('Please enter one of the following options:')
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
                    print('Input does not correspond with any option!')


if __name__ == '__main__':
    Controller()
