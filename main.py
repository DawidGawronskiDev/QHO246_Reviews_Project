"""
This module manages the overall program flow, controlling user interaction
and program behavior. It utilizes the other modules to:
- Handle user input/output via 'tui'.
- Process data via 'process'.
- Visualize data via 'visual'.
"""

from typing import Dict, List
from exporter import Review, Branch
from process import Process
from visual import Visual
from tui import TUI


class Controller:
    """
        Handles the main program flow, including user interactions, data processing,
        and visualization.

        Attributes:
            reviews (List[Review]): A list of reviews.
            branches (Dict[str, Branch]): A dictionary of branches containing reviews.
            reviewers_locations (List[str]): A list of unique reviewer locations.
    """

    def __init__(self):
        """Initializes the program and starts the main menu."""
        self.reviews: List[Review] = []
        self.branches: Dict[str, Branch] = {}
        self.reviewers_locations: List[str] = []

        self.start()

    def start(self):
        """Starts the program, loads data, and displays the main menu."""
        TUI.print_title()
        self.branches = Process.read_reviews('data/disneyland_reviews.csv')
        print(f'There are {Process.count_reviews(self.branches)} reviews.')
        while True:
            self.main_menu()

    def main_menu(self):
        """Displays the main menu and handles user selection."""
        options = Process.create_options([
            'View Data',
            'Visualise Data',
            'Export Data'
        ])
        options['X'] = 'Exit'

        actions = {
            'A': lambda: self.a_submenu(),
            'B': lambda: self.b_submenu(),
            'C': lambda: self.c_submenu(),
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
        """Displays the data viewing submenu."""
        options = Process.create_options([
            'View Reviews by Park',
            'Number of Reviews by Park and Reviewer Location',
            'Average Score per year by Park',
            'Average Score per Park by Reviewer Location'
        ])
        options['X'] = 'Go Back'

        actions = {
            'A': lambda: self.a_submenu_a(),
            'B': lambda: self.a_submenu_b(),
            'C': lambda: self.a_submenu_c(),
            'D': lambda: self.a_submenu_d(),
            'X': lambda: None
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
        """Displays reviews for a selected park."""
        branch = TUI.validate_branch(
            'For which branch would you like to see reviews?',
            list(self.branches.keys()))
        TUI.print_reviews(self.branches[branch].reviews)

    def a_submenu_b(self):
        """Displays the number of reviews by park and reviewer location."""
        branch = TUI.validate_branch(
            'For which reviewer location would you like to see number of reviews?',
            list(self.branches.keys())
        )

        location = TUI.validate_multi_choice(
            'For which reviewer location would you like to see number of reviews?',
            self.branches[branch].locations
        )

        TUI.print_reviews_count(
            branch,
            location,
            Process.filter_reviews(self.branches[branch].get_reviews(),
                                   {'branch': branch, 'reviewer_location': location})
        )

    def a_submenu_c(self):
        """Displays the average review score for a park in a selected year."""
        branch = TUI.validate_branch(
            'Select one of the following branches: ',
            list(self.branches.keys())
        )
        year = TUI.validate_multi_choice('Select one of the following years:',
                                         self.branches[branch].get_reviews_years())

        TUI.print_message(
            f'The average rating for {self.branches[branch].get_name()} branch in year {year} is {
            self.branches[branch].avg_rating}')

    def a_submenu_d(self):
        """Displays the average score per park by reviewer location."""
        TUI.print_avg_score_by_loc(self.branches)

    def b_submenu_a(self):
        """Displays a pie chart of the most reviewed parks."""
        data = Process.get_branches_reviews_count(self.branches)
        reviews_count = list(data.values())
        Visual.show_chart("pie", 'Most Reviewed Parks', labels=reviews_count, vals=reviews_count,
                          legend=[self.branches[branch].get_name() for branch in list(data.keys())])

    def b_submenu_b(self):
        """Displays a bar chart of average scores per park."""
        data = Process.get_avg_branches_rating(self.branches)
        Visual.show_chart("bar", 'Average Scores',
                          labels=[self.branches[branch].get_name() for branch in list(data.keys())],
                          vals=list(data.values()))

    def b_submenu_c(self):
        """Displays a bar chart ranking parks by nationality."""
        branch = TUI.validate_branch('Please enter one of the following options:', self.branches)
        data = self.branches[branch].top_locations

        Visual.show_chart("bar", 'Park Ranking by Nationality', labels=[item[0] for item in data],
                          vals=[item[1] for item in data])

    def b_submenu_d(self):
        """Displays a bar chart showing the most popular months by park."""
        branch = TUI.validate_branch('Please enter one of the following options:', self.branches)
        months, avg_rating = zip(*self.branches[branch].avg_popularity_by_month)

        Visual.show_chart('bar', f'Most Popular Month by Park ({self.branches[branch].get_name()})',
                          labels=list(months), vals=list(avg_rating))

    def b_submenu(self):
        """Displays the data visualization submenu."""
        options = Process.create_options([
            'Most Reviewed Parks',
            'Average Scores',
            'Park Ranking by Nationality',
            'Most Popular Month by Park'
        ])
        options['X'] = 'Go Back'

        actions = {
            'A': lambda: self.b_submenu_a(),
            'B': lambda: self.b_submenu_b(),
            'C': lambda: self.b_submenu_c(),
            'D': lambda: self.b_submenu_d(),
            'X': lambda: None
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

    def c_submenu(self):
        """Displays the export data submenu."""
        options = Process.create_options([
            'TXT',
            'CSV',
            'JSON'
        ])
        options['X'] = 'Go Back'

        actions = {
            'A': lambda: Process.export_data(self.branches, 'TXT'),
            'B': lambda: Process.export_data(self.branches, 'CSV'),
            'C': lambda: Process.export_data(self.branches, 'JSON'),
            'X': lambda: None
        }

        while True:
            TUI.print_message('Please select an export format:')
            TUI.print_options(options, 2)
            choice = TUI.handle_input()

            if choice:
                choice = choice.upper()
                if choice in actions:
                    TUI.print_confirmed_option((choice, options[choice]))
                    actions[choice]()
                    break
                else:
                    print('Input does not correspond with any option!')


if __name__ == '__main__':
    Controller()
