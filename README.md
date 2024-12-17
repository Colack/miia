# AutoShopManager

AutoShopManager is a simple application designed to manage orders for an auto shop. The application allows the user to:

- Track Orders (including customer details, vehicle information, service required, etc.)
- Add, edit, and delete orders
- Backup orders to Google Drive
- Use a clean, dark-themed UI built with `ttkbootstrap` and `tkinter`

### Features

- **Order Management**: Add new orders, update existing ones, delete them, and keep track of their status.
- **Google Drive Backup**: Backup the orders CSV file to Google Drive to ensure data safety.
- **Debugging Mode**: Enable detailed logging and debugging information with the `--debug` flag.
- **Cross-platform Compatibility**: The application is portable and can be compiled into a standalone executable for Windows, macOS, or Linux.
- **CSV File**: Stores all orders in a CSV file (`orders.csv`), which can be easily shared or imported into other systems.

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package manager)
- A Google Drive account for backing up files

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Building](#building)
5. [License](#license)

## Installation

### Step 1. Clone the Repository

First, clone the repository to your local machine:

`git clone https://github.com/colack/autoshopmanager.git`

`cd autoshopmanager`

### Step 2. Install Dependencies

Install the required Python packages using `pip`:

`pip install -r requirements.txt`

### Step 3. Set Up Google Drive Backup

To use the Google Drive backup functionality, you'll need to authenticate with Google:

1. Set up the Google API:

    - Visit the [Google Developers Console](https://console.developers.google.com/).
    - Create a new project and enable the Google Drive API.
    - Create OAuth 2.0 credentials and download the `credentials.json` file.

2. Place the `credentials.json` file in the `autoshopmanager` directory.

### Step 4. Run the Application

You can now run the application using Python:

`python main.py`

---

## Usage

### Basic Usage

- **Add a New Order**:
    - Fill in the customer name, vehicle model, service required, etc.
    - Click "Add Order" to save the order.
    
- **Edit Orders**:
    - Select an existing order from the list, modify the details, and click "Edit Order".

- **Delete Orders**:
    - Select an order from the list and click "Delete Order".

- **Backup to Google Drive**:
    - Click "Backup to Google Drive" to back up the orders to your Google Drive.

### Command-line Flags

You can use the following flags when running the application:

- **`--debug`**: Enables debugging mode and logs detailed information about the app's behavior.
  
  Example:

  `python main.py --debug`

- **`--new`**: Creates a new CSV file with the required fields if the CSV file does not exist.
  
  Example:

  `python main.py --new`

---

## Features

### Order Management
- View and manage orders (add, edit, delete) through a user-friendly interface.
- The order list includes details like customer name, vehicle model, service required, order date, notes, and completion status.

### Google Drive Backup
- The application automatically uploads the `orders.csv` file to Google Drive.
- Ensure that you authenticate with Google for this feature to work.

### Debugging Mode
- When running with the `--debug` flag, the application outputs detailed logging information, which is helpful for troubleshooting and development.

### Cross-Platform
- The app is fully cross-platform, and you can compile it into a standalone executable using the included `build.py` script. The app will work on Windows, macOS, and Linux.

---

## Building Executable

You can compile the Python script into a standalone executable using `PyInstaller`. This allows you to distribute the application without requiring users to have Python installed.

### Step 1: Build the Executable

Run the following command to create a standalone executable:

`python build.py`

This will create a folder named `dist/`, containing the executable for your operating system.

### Step 2: Run the Executable

Once the build is complete, you can run the executable from the `dist/` folder:

- **Windows**: `dist\AutoShopManager.exe`
- **macOS/Linux**: `dist/AutoShopManager`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Troubleshooting

If you encounter issues or need help:
- Make sure the required Python packages are installed.
- Ensure your `credentials.json` for Google Drive backup is correctly placed in the project directory.
- If using `--debug`, check the log for more detailed error messages.

For further assistance, you can open an issue on the GitHub repository or refer to the [documentation](https://docs.python.org/3/library/tkinter.html) for more on `tkinter`.
