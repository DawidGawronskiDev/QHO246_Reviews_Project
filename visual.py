"""
This module is responsible for visualizing data using Matplotlib.
All visualizations should be generated using functions in this module.
"""

from typing import List, Union
from exporter import Pie, Bar


class Visual:
    """
    A utility class for generating and displaying charts.

    This class provides a static method to create either Pie or Bar charts
    based on the specified chart type.

    Methods:
        show_chart(chart_type: str, title: str, labels: List[Union[str, int]], vals: List[int], legend: List[str] = None)
            Generates and displays a chart of the specified type.
    """

    def __init__(self) -> None:
        """This class is not meant to be instantiated."""
        pass

    @staticmethod
    def show_chart(chart_type: str, title: str, labels: List[Union[str, int]], vals: List[int | float],
                   legend: List[str] = None) -> None:
        """
        Creates and displays a chart of the specified type.

        Args:
            chart_type (str): The type of chart to generate. Supported types: "pie", "bar".
            title (str): The title of the chart.
            labels (List[Union[str, int]]): The labels for each data point.
            vals (List[int]): The values corresponding to each label.
            legend (List[str], optional): The legend labels for the chart. Defaults to None.

        Raises:
            ValueError: If an unsupported chart type is provided.
        """
        chart_classes = {
            "pie": Pie,
            "bar": Bar
        }

        chart_type = chart_type.lower()
        if chart_type not in chart_classes:
            raise ValueError(f"Invalid chart type '{chart_type}'. Supported types are: {list(chart_classes.keys())}")

        chart_classes[chart_type](title, labels, vals, legend)
