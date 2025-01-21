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
