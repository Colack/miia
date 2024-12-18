import os
import json
import csv
import logging

class FileManager:
    # Initialize the FileManager
    def __init__(self, data_folder="data"):
        logging.debug(f"Initializing FileManager with data folder: {data_folder}") # Debugging
        self.data_folder = data_folder
        self.metadata_file = os.path.join(data_folder, "metadata.json")
        self.ensure_data_folder()
        self.load_metadata()
        
    # Ensure the data folder exists
    def ensure_data_folder(self):
        logging.debug(f"Ensuring data folder exists: {self.data_folder}") # Debugging
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            logging.debug(f"Created data folder: {self.data_folder}") # Debugging
            
    # Load the metadata file
    def load_metadata(self):
        try:
            with open(self.metadata_file, "r") as file:
                self.metadata = json.load(file)
                logging.debug(f"Loaded metadata file: {self.metadata_file}") # Debugging
        except FileNotFoundError:
            self.metadata = {}
            self.save_metadata()
            logging.debug(f"Metadata file not found: {self.metadata_file}")
            
    # Save the metadata file
    def save_metadata(self):
        with open(self.metadata_file, "w") as file:
            json.dump(self.metadata, file, indent=4)
            logging.debug(f"Saved metadata file: {self.metadata_file}") # Debugging
            
    # Create a csv file
    def create_csv(self, name, fields):
        logging.debug(f"Creating CSV file: {name}") # Debugging
        
        # Check if fields are empty
        if not fields or not all(fields):
            logging.error("Fields are empty") # Debugging
            return False
        
        # Create the file path
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file already exists
        if name in self.metadata:
            logging.error(f"CSV file already exists: {name}") # Debugging
            return False
        
        # Check for duplicate fields
        if len(fields) != len(set(fields)):
            logging.error("Duplicate fields") # Debugging
            return False
        
        # Write the fields to the file
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            logging.debug(f"Wrote fields to CSV file: {file_path}") # Debugging
            
        # Update the metadata
        self.metadata[name] = fields
        
        # Save the metadata
        self.save_metadata()
        
        return file_path
    
    # List all csv files
    def list_csv(self):
        logging.debug("Listing CSV files") # Debugging
        return [name for name in self.metadata]

    # Get the fields of a csv file
    def get_fields(self, name):
        logging.debug(f"Getting fields of CSV file: {name}") # Debugging
        return self.metadata.get(name, [])
    
    # Read a csv file
    def read_csv(self, name):
        logging.debug(f"Reading CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return []
        
        # Read the file
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            logging.debug(f"Read CSV file: {file_path}") # Debugging
            return data
        
    # Write to a csv file
    def write_csv(self, name, data):
        logging.debug(f"Writing to CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Write to the file
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)
            logging.debug(f"Wrote to CSV file: {file_path}") # Debugging
            
    # Delete a csv file
    def delete_csv(self, name):
        logging.debug(f"Deleting CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Delete the file
        os.remove(file_path)
        logging.debug(f"Deleted CSV file: {file_path}") # Debugging
        
        # Delete the metadata
        del self.metadata[name]
        
        # Save the metadata
        self.save_metadata()
        
        return True
    
    # Rename a csv file
    def rename_csv(self, name, new_name):
        logging.debug(f"Renaming CSV file: {name} to {new_name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        new_file_path = os.path.join(self.data_folder, f"{new_name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Check if the new name already exists
        if new_name in self.metadata:
            logging.error(f"CSV file already exists: {new_name}") # Debugging
            return False
        
        # Rename the file
        os.rename(file_path, new_file_path)
        logging.debug(f"Renamed CSV file: {file_path} to {new_file_path}") # Debugging
        
        # Update the metadata
        self.metadata[new_name] = self.metadata[name]
        del self.metadata[name]
        
        # Save the metadata
        self.save_metadata()
        
        return True
    
    # Add a row to a csv file
    def add_row(self, name, row):
        logging.debug(f"Adding row to CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Add the row
        data.append(row)
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Update a row in a csv file
    def update_row(self, name, index, row):
        logging.debug(f"Updating row in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Update the row
        data[index] = row
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Delete a row from a csv file
    def delete_row(self, name, index):
        logging.debug(f"Deleting row from CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Delete the row
        del data[index]
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Search for a row in a csv file
    def search_row(self, name, field, value):
        logging.debug(f"Searching for row in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return None
        
        # Read the file
        data = self.read_csv(name)
        
        # Search for the row
        for index, row in enumerate(data):
            if row[field] == value:
                return index, row
            
        return None
    
    # Search for rows in a csv file
    def search_rows(self, name, field, value):
        logging.debug(f"Searching for rows in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return []
        
        # Read the file
        data = self.read_csv(name)
        
        # Search for the rows
        rows = []
        for index, row in enumerate(data):
            if row[field] == value:
                rows.append((index, row))
                
        return rows

    # Create a backup of the data folder
    def backup(self, folder="backup"):
        logging.debug(f"Creating backup of data folder: {folder}") # Debugging
        backup_folder = os.path.join(self.data_folder, folder)
        self.ensure_data_folder()
        
        # Check if the backup folder already exists
        if os.path.exists(backup_folder):
            logging.error(f"Backup folder already exists: {folder}") # Debugging
            return False
        
        # Copy the data folder to the backup folder
        os.system(f"cp -r {self.data_folder} {backup_folder}")
        logging.debug(f"Created backup of data folder: {folder}") # Debugging
        
        return True