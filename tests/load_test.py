import pytest
import sqlite3
import pandas as pd
from etl.load import SQLLoad

DB_PATH = "database/test_db.db"  # Use a test database
TABLE_NAME = "test_table"

@pytest.fixture
def loader():
    """Fixture to initialize SQLLoad class"""
    return SQLLoad(DB_PATH, TABLE_NAME)

@pytest.fixture
def sample_data():
    """Create sample data for loading into the database"""
    return pd.DataFrame({
        "Year": [2023, 2024],
        "Month": [1, 2],
        "Destination_Country": ["USA", "Germany"],
        "Type_of_Coffee": ["Arabica", "Robusta"],
        "Bags of 60 Kg. Exported": [500, 600]
    })

def test_load_data(loader, sample_data):
    """Check if data loads correctly into the database"""
    loader.load(sample_data)

    # Connect to the database and verify the data
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    row_count = cursor.fetchone()[0]
    
    assert row_count == 2, "Data was not loaded correctly into the database"

    conn.close()
