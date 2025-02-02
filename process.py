"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""

import csv
import json
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

    @staticmethod
    def export_data(branches, format_type: str):
        filename = f'exported_data.{format_type.lower()}'

        if format_type == 'TXT':
            with open(filename, 'w', encoding='utf-8') as f:
                for branch_name, branch in branches.items():
                    f.write(f'Branch: {branch_name}\n')
                    for review in branch.reviews:
                        f.write(
                            f'{review.review_id}, {review.rating}, {review.year_month}, {review.reviewer_location}\n')
                    f.write('\n')
            print(f'Data exported successfully to {filename}.')
        elif format_type == 'CSV':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Branch', 'Review ID', 'Rating', 'Year-Month', 'Reviewer Location'])
                for branch_name, branch in branches.items():
                    for review in branch.reviews:
                        writer.writerow(
                            [branch_name, review.review_id, review.rating, review.year_month, review.reviewer_location])
            print(f'Data exported successfully to {filename}')
        elif format_type == 'JSON':
            data = {
                branch_name: [
                    {
                        "Review ID": review.review_id,
                        "Rating": review.rating,
                        "Year-Month": review.year_month,
                        "Reviewer Location": review.reviewer_location
                    } for review in branch.reviews
                ] for branch_name, branch in branches.items()
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f'Data exported successfully to {filename}')
        else:
            print('Invalid format selected!')
