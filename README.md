# Disneyland Reviews Analyser

## Overview

Disneyland Reviews Analyser is a Python-based command-line application designed to process, analyze, and visualize
customer reviews for Disneyland parks. Users can interact with the program through a **Text User Interface (TUI)** to:

- View and filter reviews by park, location, and year.
- Generate statistical insights such as average ratings per year and location.
- Visualize data using pie charts and bar charts.
- Export processed data in **TXT, CSV, or JSON** formats.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Data Format](#data-format)
- [Contributing](#contributing)
- [License](#license)

## Features

- **View Reviews**: Search and display reviews based on Disneyland parks and reviewer locations.
- **Analyze Data**: Calculate and display average scores by year and location.
- **Visualize Data**: Generate pie and bar charts to represent review statistics.
- **Export Data**: Save processed data in TXT, CSV, or JSON format.
- **Interactive Interface**: Intuitive **TUI-based navigation** for ease of use.

## Installation

### Prerequisites

Ensure you have **Python 3.13.1** installed on your system.

### Steps

1. **Clone the repository**:
   ```sh
   git clone git@github.com:DawidGawronskiDev/QHO246_Reviews_Project.git
   cd QHO246_Reviews_Project
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```sh
   python3 main.py
   ```

## Usage

1. **Launch the application** using `python3 main.py`.
2. **Navigate the menu** by selecting an option:
    - **View Data**: Display reviews and statistics.
    - **Visualize Data**: Generate charts for better insights.
    - **Export Data**: Save processed data in a desired format.
3. **Follow on-screen instructions** to filter, select, or analyze reviews.

## Modules

The application is modularized into different components:

### **1. Controller (`controller.py`)**

Handles overall program flow, user interactions, and integration between modules.

### **2. TUI (`tui.py`)**

Manages text-based user interaction, including menu display, input validation, and formatted output.

### **3. Process (`process.py`)**

Responsible for processing review data, filtering results, and exporting data in different formats.

### **4. Visual (`visual.py`)**

Handles data visualization using Matplotlib, generating pie and bar charts.

### **5. Exporter (`exporter.py`)**

Defines data structures (`Review`, `Branch`) and handles table-based data display.

## Data Format

The application processes **Disneyland review data** in CSV format. A sample dataset (`data/disneyland_reviews.csv`) is
required, structured as follows:

```
Review ID,Rating,Year-Month,Reviewer Location,Branch
1,5,2024-01,New York,Disneyland_California
2,4,2024-02,Los Angeles,Disneyland_Paris
...
```

## License

This project is licensed under the **GNU General Public License (GPL)**. Feel free to modify and distribute it under the
terms of the GPL.