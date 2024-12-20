import os
import pandas as pd
from datetime import datetime

def generate_default_csv(file_path):
    columns = [
        "name", "contact", "address", "location", "car_model", "car_year", "car_color",
        "operation", "price", "discount", "notes", "created_at", "updated_at", "is_completed"
    ]

    default_data = [
        [
            "John Doe", "1234567890", "123 Elm St", "NY", "Toyota Corolla", "2015", "Red",
            "Oil Change", "50", "5", "N/A", datetime.now().isoformat(), datetime.now().isoformat(), "False"
        ],
        [
            "Jane Smith", "0987654321", "456 Oak St", "LA", "Honda Civic", "2018", "Blue",
            "Tire Rotation", "40", "0", "Customer requested premium tires.", datetime.now().isoformat(), datetime.now().isoformat(), "True"
        ]
    ]

    df = pd.DataFrame(default_data, columns=columns)
    df.index += 1
    df.to_csv(file_path, index_label="id")


def load_csv(file_path):
    try:
        df = pd.read_csv(file_path, index_col="id")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["discount"] = pd.to_numeric(df["discount"], errors="coerce")
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
        return df
    except Exception as e:
        raise Exception(f"Failed to load CSV file: {e}")
