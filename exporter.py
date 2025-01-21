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
    def __int__(self, branch: str, reviews: List[Review]) -> None:
        self.branch = branch
        self.reviews = reviews


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
