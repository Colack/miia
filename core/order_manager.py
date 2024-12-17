import csv
import logging
from datetime import datetime

def read_orders(file_path):
    """Read orders from the CSV file."""
    orders = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['contact'] = row.get('contact', "")
                row['notes'] = row.get('notes', "")
                row['completed'] = row.get('completed', "No")
                orders.append(row)
        logging.debug(f"Orders read successfully from {file_path}.")
    except FileNotFoundError:
        logging.warning(f"{file_path} not found. Creating a new file.")
        create_csv_file(file_path)
    except Exception as e:
        logging.error(f"Error reading orders: {e}")
    return orders

def save_orders(file_path, orders):
    """Save orders to the CSV file."""
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['order_id', 'customer_name', 'contact', 'vehicle_model', 'service_required', 'order_date', 'notes', 'completed'])
            writer.writeheader()
            writer.writerows(orders)
        logging.debug(f"Orders saved successfully to {file_path}.")
    except Exception as e:
        logging.error(f"Failed to save orders: {e}")

def create_csv_file(file_path):
    """Create a new CSV file with the appropriate headers."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['order_id', 'customer_name', 'contact', 'vehicle_model', 'service_required', 'order_date', 'notes', 'completed'])
        writer.writeheader()
    logging.debug(f"New CSV file created at {file_path}.")
