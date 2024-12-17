import os
import csv
import json

class FileManager:
    """Handles CSV and metadata files."""

    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.metadata_file = os.path.join(self.data_folder, "metadata.json")
        self.ensure_data_folder()
        self.load_metadata()

    def ensure_data_folder(self):
        """Ensure the data folder exists."""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def load_metadata(self):
        """Load metadata for CSV files."""
        try:
            with open(self.metadata_file, "r") as file:
                self.metadata = json.load(file)
        except FileNotFoundError:
            self.metadata = {}
            self.save_metadata()

    def save_metadata(self):
        """Save metadata to the JSON file."""
        with open(self.metadata_file, "w") as file:
            json.dump(self.metadata, file, indent=4)

    def create_csv(self, name, fields):
        """Create a new CSV file with specified fields."""
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        if name in self.metadata:
            raise ValueError("A file with this name already exists.")

        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

        # Add to metadata
        self.metadata[name] = {
            "file_path": file_path,
            "fields": fields
        }
        self.save_metadata()
        return file_path

    def list_csv_files(self):
        """List all available CSV files."""
        return self.metadata

    def get_csv_fields(self, name):
        """Get the fields of a CSV file."""
        return self.metadata.get(name, {}).get("fields")

    def read_csv(self, name):
        """Read data from a CSV file."""
        if name not in self.metadata:
            raise ValueError("CSV file not found.")
        file_path = self.metadata[name]["file_path"]
        data = []
        try:
            with open(file_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                data.extend(reader)
        except FileNotFoundError:
            raise ValueError(f"CSV file {name} does not exist.")
        return data

    def write_csv(self, name, rows):
        """Write data to a CSV file."""
        if name not in self.metadata:
            raise ValueError("CSV file not found.")
        file_path = self.metadata[name]["file_path"]
        fields = self.metadata[name]["fields"]

        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
