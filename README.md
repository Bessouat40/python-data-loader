# Data Ingestor Service

This project is a python service for data ingestion into a `Postgres` database.

It takes all `csv files` from a directory and insert data inside database.

## Usage

- Setup environment :

  ```bash
  mv .env.example .env
  ```

- Fill `.env` with your values

- Launch database and Python service :

  ```bash
  make start
  ```

- Put your csv file(s) inside `data`folder and then run :

  ```bash
  python utils/ingest.py
  ```

**Now you can call your Data Ingestor Service !!!**

### Results

```bash
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
---------- Start Data Ingestion ----------


We found 3 csv files to process


-------------------------


2 lines from .../data-ingestor-service/data/test.csv inserted into test
.../data-ingestor-service/fastapi_service/postgresIngestor.py:57: UserWarning: We can't add data from .../data-ingestor-service/data/test2.csv, columns doesn't match tables from public schema...
  warnings.warn(f"We can't add data from {path}, columns doesn't match tables from {SCHEMA} schema...")
2 lines from .../data-ingestor-service/data/test_copy.csv inserted into test


-------------------------


Total : 4 inserted lines


---------- End Data Ingestion ----------
INFO:     127.0.0.1:64419 - "POST /ingest HTTP/1.1" 200 OK
```
