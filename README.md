# Miia

Miia is a Python application that allows you to view, search, add, edit, and delete rows in a CSV file using a graphical user interface (GUI) built with Tkinter.

## Features

- **Dark Mode**: The application uses a dark theme for the GUI.
- **CSV Auto-Generation**: Automatically generates a default CSV file if it doesn't exist.
- **Search Functionality**: Search for specific rows in the CSV file.
- **Row Management**: Add, edit, and delete rows in the CSV file.
- **Inline Editing**: Double-click on a cell to edit its value directly.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`):
  - `tkinter`
  - `pandas`
  - `pyautogui`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/colack/miia.git
    cd miia
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    python miia.py
    ```

2. The application will open a window displaying the contents of data.csv. If data.csv does not exist, it will be created with default data.

3. Use the search bar to filter rows based on your query.

4. Use the "Add", "Edit", and "Delete" buttons to manage rows in the CSV file.
