"""
This module is responsible for processing the data.

It receives the dataset and performs necessary operations to provide the desired results
in the required format. This includes data filtering, counting, and exporting.

Functions:
- Load and parse reviews from a CSV file.
- Perform operations on the dataset, such as filtering and counting.
- Export processed data in TXT, CSV, or JSON format.
"""

import csv
import json
from typing import List, Dict, Union
from exporter import Branch, Review


class Process:
    """
    A utility class for handling data processing operations.

    This class provides methods to load, filter, count, and export reviews
    in different formats.
    """

    def __init__(self) -> None:
        """This class is not meant to be instantiated."""
        pass

    @staticmethod
    def read_reviews(file_path: str) -> Dict[str, Branch]:
        """
        Reads review data from a CSV file and structures it into a dictionary of Branch objects.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            Dict[str, Branch]: A dictionary where keys are branch names and values are Branch objects.
        """
        print('Loading reviews...')
        with open(file_path, encoding="utf-8") as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Skip the header row

            branches: Dict[str, Branch] = {}

            for review in csvreader:
                review_id, rating, year_month, reviewer_location, branch = review

                if branch not in branches:
                    branches[branch] = Branch(branch, [])

                branches[branch].reviews.append(
                    Review(int(review_id), int(rating), year_month, reviewer_location, branch)
                )

        print('Loading finished!')
        return branches

    @staticmethod
    def count_reviews(branches: Dict[str, Branch]) -> int:
        """
        Counts the total number of reviews across all branches.

        Args:
            branches (Dict[str, Branch]): A dictionary of Branch objects.

        Returns:
            int: Total number of reviews.
        """
        return sum(branch.review_count for branch in branches.values())

    @staticmethod
    def create_options(items: Union[Dict[str, Branch], List[str]]) -> Dict[str, str]:
        """
        Maps items to English alphabet letters (A-Z) for user selection.

        Args:
            items (Union[Dict[str, Branch], List[str]]): A list or dictionary of options.

        Returns:
            Dict[str, str]: A dictionary mapping letters (A-Z) to items.

        Raises:
            ValueError: If the number of items exceeds 26.
        """
        max_len = 26
        if len(items) > max_len:
            raise ValueError(f'Options list is too long! Maximum allowed is: {max_len}')

        return {chr(i + 65): item for i, item in enumerate(items)}

    @staticmethod
    def trans_str(s: str) -> str:
        """
        Normalizes a string by converting it to lowercase, removing spaces, and replacing underscores.

        Args:
            s (str): The input string.

        Returns:
            str: The normalized string.
        """
        return ''.join(s.lower().split()).replace('_', '')

    @staticmethod
    def filter_reviews(reviews: List[Review], filters: Dict[str, str]) -> List[Review]:
        """
        Filters reviews based on specified criteria.

        Args:
            reviews (List[Review]): List of reviews to be filtered.
            filters (Dict[str, str]): A dictionary containing filter keys and values.

        Returns:
            List[Review]: A list of reviews that match the specified filters.
        """
        filtered_reviews = []

        for review in reviews:
            if 'year' in filters and not review.year_month.startswith(filters['year']):
                continue
            if all(Process.trans_str(vars(review)[key]) == Process.trans_str(value)
                   for key, value in filters.items() if key != 'year'):
                filtered_reviews.append(review)

        return filtered_reviews

    @staticmethod
    def get_branches_reviews_count(branches: Dict[str, Branch]) -> Dict[str, int]:
        """
        Retrieves the number of reviews for each branch.

        Args:
            branches (Dict[str, Branch]): A dictionary of Branch objects.

        Returns:
            Dict[str, int]: A dictionary where keys are branch names and values are review counts.
        """
        return {branch_name: branch.review_count for branch_name, branch in branches.items()}

    @staticmethod
    def get_avg_branches_rating(branches: Dict[str, Branch]) -> Dict[str, float]:
        """
        Retrieves the average rating for each branch.

        Args:
            branches (Dict[str, Branch]): A dictionary of Branch objects.

        Returns:
            Dict[str, float]: A dictionary where keys are branch names and values are average ratings.
        """
        return {branch_name: branch.avg_rating for branch_name, branch in branches.items()}

    @staticmethod
    def export_data(branches: Dict[str, Branch], format_type: str) -> None:
        """
        Exports review data to a file in TXT, CSV, or JSON format.

        Args:
            branches (Dict[str, Branch]): A dictionary of Branch objects containing review data.
            format_type (str): The format for exporting the data (TXT, CSV, JSON).

        Raises:
            ValueError: If an invalid format is specified.
        """
        filename = f'exported_data.{format_type.lower()}'

        if format_type.upper() == 'TXT':
            with open(filename, 'w', encoding='utf-8') as f:
                for branch_name, branch in branches.items():
                    f.write(f'Branch: {branch_name}\n')
                    for review in branch.reviews:
                        f.write(
                            f'{review.review_id}, {review.rating}, {review.year_month}, {review.reviewer_location}\n')
                    f.write('\n')
            print(f'Data exported successfully to {filename} (TXT format).')

        elif format_type.upper() == 'CSV':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Branch', 'Review ID', 'Rating', 'Year-Month', 'Reviewer Location'])
                for branch_name, branch in branches.items():
                    for review in branch.reviews:
                        writer.writerow(
                            [branch_name, review.review_id, review.rating, review.year_month, review.reviewer_location])
            print(f'Data exported successfully to {filename} (CSV format).')

        elif format_type.upper() == 'JSON':
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
            print(f'Data exported successfully to {filename} (JSON format).')

        else:
            raise ValueError(f"Invalid format '{format_type}'. Supported formats: TXT, CSV, JSON.")
