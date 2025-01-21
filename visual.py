"""
This module is responsible for visualising the data using Matplotlib.
Any visualisations should be generated via functions in this module.
"""

from typing import List
import matplotlib.pyplot as plt
import numpy as np


class Visual:
    def __init__(self):
        pass

    @staticmethod
    def show_most_reviewed_parks(labels: List[str], vals: List[int], legend: List[str] = None) -> None:
        fig, ax = plt.subplots()

        # plot values and labels
        ax.pie(vals, labels=labels)

        # Set title
        ax.set_title('Most Review Parks')

        # create legend
        if legend:
            ax.legend(legend)

        # show figure
        plt.show()

    @staticmethod
    def show_avg_reviews(labels: List[str], vals: List[int], legend: List[str] = None) -> None:
        fig, ax = plt.subplots()

        # plot values and labels
        ax.bar(labels, vals)

        # Set title
        ax.set_title('Average Scores')

        # create legend
        if legend:
            ax.legend(legend)

        # show figure
        plt.show()
