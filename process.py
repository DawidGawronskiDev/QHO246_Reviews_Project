"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""

import csv
from typing import List

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
        print('Loading...')
        with open(file_path) as f:
            csvreader = csv.reader(f)
            csvreader.__next__()
            reviews = []
            for review in csvreader:
                review_id, rating, year_month, reviewer_location, branch = review
                reviews.append(Review(int(review_id), int(rating), year_month, reviewer_location, branch))
        print('Loading finished!')
        return reviews