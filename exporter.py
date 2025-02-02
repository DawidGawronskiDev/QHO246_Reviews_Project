from typing import List, Tuple, Dict
import matplotlib.pyplot as plt


class Review:
    """
    Represents a customer review.

    Attributes:
        review_id (int): Unique identifier for the review.
        rating (int): Rating given by the reviewer (1-5 scale).
        year_month (str): Review timestamp in "YYYY-MM" format.
        reviewer_location (str): Location of the reviewer.
        branch (str): Branch where the review was given.
    """

    def __init__(self, review_id: int, rating: int, year_month: str, reviewer_location: str, branch: str) -> None:
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
                f'Branch: {self.branch.replace("_", " ")}')


class Branch:
    """
    Represents a branch and its associated reviews.

    Attributes:
        branch (str): The name of the branch.
        reviews (List[Review]): A list of reviews associated with this branch.
    """

    def __init__(self, branch: str, reviews: List[Review]) -> None:
        self.branch = branch
        self.reviews = reviews

    def get_reviews(self) -> List[Review]:
        """Returns a copy of the reviews list."""
        return list(self.reviews)

    @property
    def locations(self) -> List[str]:
        """Returns a list of unique reviewer locations."""
        return list({review.reviewer_location for review in self.reviews})

    def get_reviews_years(self) -> List[str]:
        """Returns a sorted list of unique years from the reviews."""
        return sorted({review.year_month.split('-')[0] for review in self.reviews})

    @property
    def avg_rating(self) -> float:
        """Calculates and returns the average rating for the branch."""
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1) if self.reviews else 0

    @property
    def avg_rating_by_loc(self) -> Dict[str, float]:
        """Calculates and returns the average rating per reviewer location."""
        ratings = {location: {'sum': 0, 'count': 0} for location in self.locations}

        for review in self.reviews:
            loc = review.reviewer_location
            ratings[loc]['sum'] += review.rating
            ratings[loc]['count'] += 1

        return {k: round(v['sum'] / v['count'], 1) if v['count'] > 0 else 0 for k, v in ratings.items()}

    @property
    def review_count(self) -> int:
        """Returns the total number of reviews."""
        return len(self.reviews)

    @property
    def top_locations(self) -> List[Tuple[str, float]]:
        """Returns the top 10 reviewer locations sorted by average rating."""
        locations = {loc: {'sum': 0, 'count': 0} for loc in self.locations}

        for review in self.reviews:
            locations[review.reviewer_location]['sum'] += review.rating
            locations[review.reviewer_location]['count'] += 1

        averages = {k: round(v['sum'] / v['count'], 1) for k, v in locations.items() if v['count'] > 0}
        return sorted(averages.items(), key=lambda x: x[1], reverse=True)[:10]

    def get_name(self) -> str:
        """Returns the formatted branch name."""
        return self.branch.replace('_', ' ')

    @property
    def avg_popularity_by_month(self) -> List[Tuple[str, float]]:
        """Returns the average rating per month, ensuring all months are included."""
        months_tuple = ('January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December')

        monthly_ratings = {month: {'sum': 0, 'count': 0} for month in months_tuple}

        for review in self.reviews:
            if review.year_month == 'missing':
                continue

            month_name = months_tuple[int(review.year_month.split('-')[1]) - 1]
            monthly_ratings[month_name]['sum'] += review.rating
            monthly_ratings[month_name]['count'] += 1

        return [(month, round(data['sum'] / data['count'], 1) if data['count'] > 0 else 0) for month, data in
                monthly_ratings.items()]


class Chart:
    """
    Base class for different types of charts.

    Attributes:
        title (str): Chart title.
        labels (List[str]): Labels for the data.
        vals (List[int]): Values associated with the labels.
        legend (List[str], optional): Legend labels.
    """

    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None) -> None:
        self.title = title
        self.labels = labels
        self.vals = vals
        self.legend = legend

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.title)

    def show(self) -> None:
        """Displays the chart."""
        plt.show()


class Pie(Chart):
    """Generates a Pie chart."""

    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None):
        super().__init__(title, labels, vals, legend)
        self.create()

    def create(self) -> None:
        """Creates and displays the pie chart."""
        self.ax.pie(self.vals, labels=self.labels)
        if self.legend:
            self.ax.legend(self.legend)
        self.show()


class Bar(Chart):
    """Generates a Bar chart."""

    def __init__(self, title: str, labels: List[str], vals: List[int], legend: List[str] = None):
        super().__init__(title, labels, vals, legend)
        self.create()

    def create(self) -> None:
        """Creates and displays the bar chart."""
        self.ax.bar(self.labels, self.vals)
        if self.legend:
            self.ax.legend(self.legend)
        self.show()


class Table:
    """
    Represents a formatted table for displaying data.

    Attributes:
        headers (List[str]): Column headers.
        rows (List[List[str]]): Rows of data.
        lengths (List[int]): Column widths.
    """

    def __init__(self, headers: List[str], rows: List[List[str]], lengths: List[int]) -> None:
        self.headers = headers
        self.rows = rows
        self.lengths = lengths

    def __str__(self) -> str:
        """Returns the table as a formatted string."""
        header = self.create_row(self.headers)
        border = '#' * len(header)
        rows_str = '\n'.join(self.create_row(row) for row in self.rows)
        return f"{border}\n{header}\n{border}\n{rows_str}\n{border}"

    def create_row(self, items: List[str]) -> str:
        """Formats a single row with proper column spacing."""
        formatted_columns = [str(column).ljust(length) for column, length in zip(items, self.lengths)]
        return f"# {' # '.join(formatted_columns)} #"

    def print_header(self) -> None:
        """Prints the table header."""
        header = self.create_row(self.headers)
        border = '#' * len(header)
        print(f"{border}\n{header}\n{border}")

    def print_row(self, items: List[str]) -> None:
        """Prints a single row of data."""
        print(self.create_row(items))
