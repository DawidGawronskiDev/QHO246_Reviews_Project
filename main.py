"""
This module is responsible for the overall program flow. It controls how the user interacts with the
program and how the program behaves. It uses the other modules to interact with the user, carry out
processing, and for visualising information.

Note:   any user input/output should be done in the module 'tui'
        any processing should be done in the module 'process'
        any visualisation should be done in the module 'visual'
"""

from typing import List
from process import Process, Review

class Controller:
    def __init__(self):
        self.reviews: List[Review] = []

        self.start()

    def start(self):
        self.reviews = Process.read_reviews('data/disneyland_reviews.csv')

if __name__ == '__main__':
    Controller()