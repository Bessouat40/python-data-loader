from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv, find_dotenv
from pandas import read_csv
from os import environ, listdir
import warnings

load_dotenv(find_dotenv())

POSTGRES_USER=environ.get("POSTGRES_USER")
POSTGRES_PASSWORD=environ.get("POSTGRES_PASSWORD")
POSTGRES_DB=environ.get("POSTGRES_DB")
HOST=environ.get("API_HOST")
PORT=environ.get("PORT")
SCHEMA=environ.get("SCHEMA")
DATA_FOLDER="/data"

class PostgresIngestor:

    def __init__(self) :
        self.engine = create_engine(f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}")
        self.conn = self.engine.connect()
        self.inspector = inspect(self.engine)
        self.schemas = self.inspector.get_schema_names()
        self.tables_columns = {}
        self.nbr_insert = 0
        self.get_columns()

    def get_columns(self):
        for schema in self.schemas :
            tables = self.inspector.get_table_names(schema=schema)
            for table in tables :
                columns = self.inspector.get_columns(table, schema)
                names = sorted([column['name'] for column in columns])
                self.tables_columns[table] = names

    def find_keys_by_values(self, values_list):
        matching_keys = None
        for key, lst in self.tables_columns.items():
            if all(value in lst for value in values_list):
                return key
        return matching_keys

    @staticmethod
    def get_data_list(path) :
        data_list = listdir(path)
        csv_list = [path + "/" + data for data in data_list if data.endswith('.csv')]
        return csv_list
    
    def put_csv(self, path):
        df = read_csv(path, sep=';')
        cols = sorted(df.columns)
        table = self.find_keys_by_values(cols)
        if table :
            nbr_insert = df.to_sql(name=table, schema=SCHEMA, con=self.conn, if_exists="append", index=False)
            print(f'{nbr_insert} lines from {path} inserted into {table} ')
            self.nbr_insert += nbr_insert
        else :
            warnings.warn(f"We can't add data from {path}, columns doesn't match tables from {SCHEMA} schema...")

    def ingest_data(self):
        print("---------- Start Data Ingestion ----------")
        self.nbr_insert = 0
        csv_list = self.get_data_list(DATA_FOLDER)
        print('\n')
        print(f'We found {len(csv_list)} csv files to process')
        print('\n')
        print("-" * 25)
        print('\n')
        [self.put_csv(csv) for csv in csv_list]
        print('\n')
        print("-" * 25)
        print('\n')
        print(f"Total : {self.nbr_insert} inserted lines")
        print('\n')
        print("---------- End Data Ingestion ----------")
