"""
TUI (Text-User Interface) Module

This module is responsible for communicating with the user.
It displays information and retrieves user input while handling any errors or invalid inputs.
No data processing should be performed here.

Functions:
- Display messages, options, and structured data (tables).
- Handle user input and validation.
- Format outputs appropriately.
"""

from typing import Dict, List, Union
from exporter import Review, Branch, Table
from process import Process


class TUI:
    """
    A utility class for handling text-based user interaction.

    Provides methods to display messages, options, and formatted tables,
    as well as handling and validating user input.
    """

    def __init__(self) -> None:
        """This class is not meant to be instantiated."""
        pass

    @staticmethod
    def print_title() -> None:
        """Prints the application title with a decorative line."""
        title = 'Disneyland Reviews Analyser'
        line = '-' * len(title)
        print(f'{line}\n{title}\n{line}')

    @staticmethod
    def print_options(options: Union[Dict[str, str], List[str]], indent: int = 0) -> None:
        """
        Displays available options to the user.

        Args:
            options (Union[Dict[str, str], List[str]]): A dictionary of labeled options or a list of options.
            indent (int, optional): Number of tab spaces for indentation. Defaults to 0.

        Raises:
            ValueError: If indent is negative.
        """
        if indent < 0:
            raise ValueError('Indent value must be greater than or equal to 0!')

        if isinstance(options, dict):
            for key, value in options.items():
                print(f"{'\t' * indent}[{key}] {value.replace('_', ' ')}")
        else:
            for value in options:
                print(f"{'\t' * indent}- {value.replace('_', ' ')}")

    @staticmethod
    def print_message(message: str) -> None:
        """Displays a message to the user."""
        print(message)

    @staticmethod
    def handle_input() -> Union[str, None]:
        """
        Retrieves user input, ensuring it's not empty.

        Returns:
            Union[str, None]: The user input string if valid, otherwise None.
        """
        user_input = input().strip()

        if not user_input:
            print("Input cannot be empty!")
            return None
        return user_input

    @staticmethod
    def print_confirmed_option(option: Union[str, Tuple[str, str]]) -> None:
        """
        Displays the selected option confirmation.

        Args:
            option (Union[str, Tuple[str, str]]): Either a string option or a tuple with a key and description.
        """
        if isinstance(option, str):
            print(f'You have chosen option - {option}')
        else:
            print(f'You have chosen option {option[0]} - {option[1]}')

    @staticmethod
    def print_reviews(reviews: List[Review]) -> None:
        """
        Displays reviews in a formatted table.

        Args:
            reviews (List[Review]): List of reviews to display.
        """
        if not reviews:
            print("No reviews available.")
            return

        headers = list(vars(reviews[0]).keys())
        rows = [list(vars(review).values()) for review in reviews]
        column_widths = [16, 8, 16, 32]

        print(Table(headers, rows, column_widths))

    @staticmethod
    def print_reviews_count(branch: str, loc: str, reviews: List[Review]) -> None:
        """
        Displays the number of reviews for a given branch and location.

        Args:
            branch (str): The branch name.
            loc (str): The reviewer location.
            reviews (List[Review]): List of matching reviews.
        """
        print(f'There are {len(reviews)} reviews from reviewers in {loc} for {branch.replace("_", " ")} branch.')

    @staticmethod
    def validate_branch(msg: str, branches: Union[Dict[str, Branch], List[str]]) -> str:
        """
        Validates and retrieves a selected branch from user input.

        Args:
            msg (str): The message prompt for the user.
            branches (Union[Dict[str, Branch], List[str]]): Available branches.

        Returns:
            str: The selected branch name.
        """
        branch_options = Process.create_options(branches)

        while True:
            TUI.print_message(msg)
            TUI.print_options(branch_options, 3)
            choice = TUI.handle_input()

            if choice:
                choice = choice.upper()
                if choice in branch_options:
                    selected_branch = branch_options[choice]
                    TUI.print_confirmed_option(selected_branch.replace('_', ' '))
                    return selected_branch
                else:
                    print('Input does not correspond with any option!')

    @staticmethod
    def print_avg_score_by_loc(branches: Dict[str, Branch]) -> None:
        """
        Displays the average rating per reviewer location in a formatted table.

        Args:
            branches (Dict[str, Branch]): Dictionary of branches with review data.
        """
        headers = ['Park', 'Reviewer Location', 'Average Rating']
        rows = [[branch_name, *rating] for branch_name, branch in branches.items() for rating in
                branch.avg_rating_by_loc.items()]
        column_widths = [32, 48, 16]

        print(Table(headers, rows, column_widths))

    @staticmethod
    def validate_multi_choice(msg: str, options: List[str]) -> str:
        """
        Validates and retrieves a selected option from the user.

        Args:
            msg (str): The message prompt for the user.
            options (List[str]): The available options.

        Returns:
            str: The validated choice.
        """
        while True:
            TUI.print_options(options, 3)
            TUI.print_message(msg)
            choice = TUI.handle_input()

            if choice:
                normalized_choice = Process.trans_str(choice)
                for option in options:
                    if normalized_choice == Process.trans_str(option):
                        TUI.print_confirmed_option(option)
                        return option
                print('Input does not correspond with any option!')
