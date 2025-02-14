from sqlalchemy import create_engine
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


db_path = "database/exportations.db"
table_name = "colombian_coffee_exports"  

class SQLLoad:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    def load(self, data):
        
        if data is None or data.empty:
            logging.warning("No data to load. Skipping database write.")
            return

        try:
            # Create SQLite connection
            engine = create_engine(f'sqlite:///{self.db_path}')
            logging.info(f"Connecting to database at {self.db_path}...")

            # Load data into the SQL table
            with engine.begin() as conn:
                data.to_sql(self.table_name, con=conn, if_exists='replace', index=False)
            
            logging.info(f"Data successfully loaded into table: {self.table_name}")

        except Exception as e:
            logging.error(f"Error loading data into the database: {e}")
