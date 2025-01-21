"""
This module is responsible for the overall program flow. It controls how the user interacts with the
program and how the program behaves. It uses the other modules to interact with the user, carry out
processing, and for visualising information.

Note:   any user input/output should be done in the module 'tui'
        any processing should be done in the module 'process'
        any visualisation should be done in the module 'visual'
"""

from typing import List
from exporter import Review
from process import Process
from visual import Visual
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
            'D': lambda: self.a_submenu_d()
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

    def a_submenu_d(self):
        """
            This code must be refactored
        """
        branches = {}
        for review in self.reviews:
            if review.branch not in branches:
                branches[review.branch] = {}
            else:
                if review.reviewer_location not in branches[review.branch]:
                    branches[review.branch][review.reviewer_location] = [0, 0]  # sum rating & reviews count
                else:
                    branches[review.branch][review.reviewer_location][0] += review.rating
                    branches[review.branch][review.reviewer_location][1] += 1

        for branch_name, locations in branches.items():
            print(branch_name)
            for location, score in locations.items():
                if score[1] != 0:
                    print(location, round(score[0] / score[1], 1))
                else:
                    print(location, 0)

    def b_submenu_a(self):
        data = Process.get_branches_reviews_count(self.branches, self.reviews)
        branches = [branch.replace('_', ' ') for branch in list(data.keys())]
        reviews_count = list(data.values())
        Visual.show_most_reviewed_parks(labels=reviews_count, vals=reviews_count, legend=branches)

    def b_submenu_b(self):
        data = Process.get_avg_branches_rating(self.branches, self.reviews)
        branches = [branch.replace('_', ' ') for branch in list(data.keys())]
        avg_reviews = list(data.values())
        Visual.show_avg_reviews(labels=branches, vals=avg_reviews)

    def b_submenu_c(self):
        branch = TUI.validate_branch('Please enter one of the following options:', self.branches)
        data = Process.get_top_branch_locations(branch, self.reviews, 10)
        locations = [item[0] for item in data]
        average_ratings = [item[1] for item in data]

        print(locations, average_ratings)

        Visual.show_park_ranking_by_nationality(labels=locations, vals=average_ratings)

    def b_submenu(self):
        message = 'Please enter one of the following options:'
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
