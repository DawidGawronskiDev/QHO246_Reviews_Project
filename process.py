"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""

import csv
from exporter import Review
from typing import List, Dict


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
    def get_branches(reviews: List[Review]) -> List[str]:
        branches = []
        for review in reviews:
            if review.branch not in branches:
                branches.append(review.branch)
        return branches

    def get_reviewers_locations(reviews: List[Review]) -> List[str]:
        locations = []
        for review in reviews:
            if review.reviewer_location not in locations:
                locations.append(review.reviewer_location)
        return locations

    @staticmethod
    def get_branch_reviews(branch: str, reviews: List[Review]) -> List[Review]:
        return [review for review in reviews if
                Process.trans_str(review.branch) == Process.trans_str(branch)]

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
    def get_reviews_years(branch: str, reviews: List[Review]):
        filtered_reviews = Process.filter_reviews(reviews, {'branch': branch})

        years = []
        for review in filtered_reviews:
            year = review.year_month.split('-')[0]
            if year not in years:
                years.append(year)

        return sorted(years)

    @staticmethod
    def get_avg_rating(reviews: List[Review]) -> float:
        if len(reviews) <= 0:
            return 0

        return round(sum([review.rating for review in reviews]) / len(reviews), 1)

    @staticmethod
    def get_branches_reviews_count(branches: List[str], reviews: List[Review]) -> Dict[str, int]:
        counts = {}
        for branch in branches:
            counts[branch] = 0

        for review in reviews:
            if review.branch in counts:
                counts[review.branch] += 1
        return counts

    @staticmethod
    def get_avg_branches_rating(branches: List[str], reviews: List[Review]):
        avg_ratings = {}
        for branch in branches:
            avg_ratings[branch] = {'sum_reviews': 0, 'count': 0}

        for review in reviews:
            avg_ratings[review.branch]['count'] += 1
            avg_ratings[review.branch]['sum_reviews'] += review.rating

        return {k: round(v['sum_reviews'] / v['count'], 1) if v['count'] > 0 else 0 for k, v in
                list(avg_ratings.items())}
