"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""

import csv
from exporter import Branch, Review
from typing import List, Dict


class Process:
    def __init__(self):
        pass

    @staticmethod
    def read_reviews(file_path: str) -> Dict[str, Branch]:
        print('Loading reviews...')
        with open(file_path) as f:
            csvreader = csv.reader(f)
            csvreader.__next__()
            branches = {}
            for review in csvreader:
                review_id, rating, year_month, reviewer_location, branch = review

                if branch not in branches:
                    branches[branch] = Branch(branch, [])

                branches[branch].reviews.append(
                    Review(int(review_id), int(rating), year_month, reviewer_location, branch))

        print('Loading finished!')
        return branches

    @staticmethod
    def count_reviews(branches):
        count = 0
        for branch in branches.values():
            count += branch.review_count
        return count

    @staticmethod
    def create_options(items: Dict[str, Branch] | List[str]) -> Dict[str, str]:
        """
            Generates dictionary that maps items to English alphabet letters (A-Z).

            Args:
                items (List[str]): List of options to be mapped to English alphabet letters.

            Returns:
                Dict[str, str]: A dictionary of options mapped to letters.

            Raises:
                ValueError: if items list is longer than 26.
        """
        max_len = 26
        if len(items) > max_len:
            raise ValueError(f'Options list is too long! Maximum number is: {max_len}')
        options = {}
        for i, item in enumerate(items):
            options[chr(i + 65)] = item
        return options

    @staticmethod
    def trans_str(s: str) -> str:
        return ''.join(s.lower().split()).replace('_', '')

    @staticmethod
    def filter_reviews(reviews: List[Review], filters: Dict[str, str]) -> List[Review]:
        filtered_reviews = []

        for review in reviews:
            if 'year' in filters:
                if not review.year_month.startswith(filters['year']):
                    continue
            if all(Process.trans_str(vars(review)[k]) == Process.trans_str(v) for k, v in filters.items() if
                   k != 'year'):
                filtered_reviews.append(review)

        return filtered_reviews

    @staticmethod
    def get_branches_reviews_count(branches: Dict[str, Branch]) -> Dict[str, int]:
        return {k: v.review_count for k, v in branches.items()}

    @staticmethod
    def get_avg_branches_rating(branches: Dict[str, Branch]):
        return {k: v.avg_rating for k, v in branches.items()}
