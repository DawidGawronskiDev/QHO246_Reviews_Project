from typing import List
import matplotlib.pyplot as plt


class Review:
    def __init__(self, review_id: int, rating: int, year_month: str, reviewer_location: str, branch: str):
        self.review_id = review_id
        self.rating = rating
        self.year_month = year_month
        self.reviewer_location = reviewer_location
        self.branch = branch

    def __str__(self) -> str:
        return (f'Review ID: {self.review_id}. '
                f'Rating: {self.rating}. '
                f'Date: {self.year_month}. '
                f'Reviewer Location: {self.reviewer_location}. '
                f'Branch: {self.branch.replace('_', ' ')}')


class Branch:
    def __init__(self, branch: str, reviews: List[Review]) -> None:
        self.branch = branch
        self.reviews = reviews

    def get_reviews(self) -> List[Review]:
        return list(self.reviews)

    def get_locations(self) -> List[str]:
        locations = []
        for review in self.reviews:
            if review.reviewer_location not in locations:
                locations.append(review.reviewer_location)
        return locations

    def get_reviews_years(self):
        years = []
        for review in self.reviews:
            year = review.year_month.split('-')[0]
            if year not in years:
                years.append(year)
        return sorted(years)

    def get_avg_rating(self) -> float:
        if len(self.reviews) <= 0:
            return 0
        return round(sum([review.rating for review in self.reviews]) / len(self.reviews), 1)

    def get_avg_rating_by_loc(self):
        avg_ratings = {location: {'sum': 0, 'count': 0} for location in self.get_locations()}

        for review in self.reviews:
            loc = review.reviewer_location
            if loc in avg_ratings:
                avg_ratings[loc]['sum'] += review.rating
                avg_ratings[loc]['count'] += 1

        return {k: round(v['sum'] / v['count'], 1) if v['count'] > 0 else 0 for k, v in avg_ratings.items()}

    def get_review_count(self):
        return len(self.reviews)

    def get_top_locations(self, limit: int = None):
        locations = {}
        for review in self.reviews:
            loc = review.reviewer_location
            if loc not in locations:
                locations[loc] = {'sum': 0, 'count': 0}

            if loc in locations:
                locations[loc]['sum'] += review.rating
                locations[loc]['count'] += 1

        locations_averages = {k: round(v['sum'] / v['count'], 1) if v['count'] > 0 else 0 for k, v in locations.items()}

        sorted_locations = sorted(locations_averages.items(), key=lambda i: i[1], reverse=True)

        if limit:
            return sorted_locations[:limit]
        else:
            return sorted_locations

    def get_name(self):
        return self.branch.replace('_', ' ')


class Chart:
    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None) -> None:
        self.title = title
        self.labels = labels
        self.vals = vals
        self.legend = legend

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.title)

    def show(self):
        plt.show()


class Pie(Chart):
    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None):
        super().__init__(title, labels, vals, legend)
        self.create()

    def create(self):
        self.ax.pie(self.vals, labels=self.labels)
        if self.legend:
            self.ax.legend(self.legend)

        self.show()


class Bar(Chart):
    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None):
        super().__init__(title, labels, vals, legend)
        self.create()

    def create(self):
        self.ax.bar(self.labels, self.vals)
        if self.legend:
            self.ax.legend(self.legend)

        self.show()


class Table:
    def __init__(self, headers: List[str], rows: List[List[str]], lengths: List[int]) -> None:
        """
        Initializes a table for formatted display.

        Args:
            headers (List[str]): The headers of the table.
            rows (List[List[str]]): The rows of data to be displayed.
            lengths (List[int]): The widths of each column.
        """
        self.headers = headers
        self.rows = rows
        self.lengths = lengths

    def __str__(self) -> str:
        """
        Returns a string representation of the table with borders and formatted rows.
        """
        header = self.create_row(self.headers)
        border = '#' * len(header)
        rows_str = '\n'.join(self.create_row(row) for row in self.rows)

        return f"{border}\n{header}\n{border}\n{rows_str}\n{border}"

    def create_row(self, items: List[str]) -> str:
        """
        Creates a formatted row with the specified column widths.

        Args:
            items (List[str]): A list of items to be formatted into a row.

        Returns:
            str: The formatted row as a string.
        """
        formatted_columns = [str(column).ljust(length) for column, length in zip(items, self.lengths)]
        return f"# {' # '.join(formatted_columns)} #"

    def print_header(self) -> None:
        """
        Prints the header of the table to the console.
        """
        header = self.create_row(self.headers)
        border = '#' * len(header)
        print(f"{border}\n{header}\n{border}")

    def print_row(self, items: List[str]) -> None:
        """
        Prints a row of data to the console.

        Args:
            items (List[str]): A list of items to be printed as a row.
        """
        print(self.create_row(items))
