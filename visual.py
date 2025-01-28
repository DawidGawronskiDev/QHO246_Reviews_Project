"""
This module is responsible for visualising the data using Matplotlib.
Any visualisations should be generated via functions in this module.
"""

from typing import List
from exporter import Pie, Bar


class Visual:
    def __init__(self):
        pass

    @staticmethod
    def show_chart(chart_type: str, title, labels: List[str | int], vals: List[int], legend: List[str] = None):
        chart_classes = {
            "pie": Pie,
            "bar": Bar
        }
        if chart_type.lower() not in chart_classes:
            raise ValueError(f"Invalid chart type '{chart_type}'. Supported types are: {list(chart_classes.keys())}")

        chart_classes[chart_type.lower()](title, labels, vals, legend)
