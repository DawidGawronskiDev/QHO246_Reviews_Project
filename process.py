"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""

import csv
from typing import List, Dict


class Review:
    def __init__(self, review_id: int, rating: int, year_month: str, reviewer_location: str, branch: str):
        self.review_id = review_id
        self.rating = rating
        self.year_month = year_month
        self.reviewer_location = reviewer_location
        self.branch = branch


class Process:
    def __init__(self):
        pass

    @staticmethod
    def read_reviews(file_path: str) -> List[Review]:
        print('Loading reviews...')
        with open(file_path) as f:
            csvreader = csv.reader(f)
            csvreader.__next__()
            reviews = []
            for review in csvreader:
                review_id, rating, year_month, reviewer_location, branch = review
                reviews.append(Review(int(review_id), int(rating), year_month, reviewer_location, branch))
        print('Loading finished!')
        return reviews

    @staticmethod
    def create_options(items: List[str]) -> Dict[str, str]:
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
