from fastapi import FastAPI, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from postgresIngestor import PostgresIngestor
from elasticIngestor import ElasticIngestor

app = FastAPI()

# pgIngestor = PostgresIngestor()
elasticIngestor = ElasticIngestor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestDataRequest(BaseModel):
    path: str

# @app.get('/ingestPostgres')
# async def get_data():
#     pgIngestor.ingest_data()
#     return Response(status_code=200)

@app.get('/ingestElastic')
async def get_data():
    elasticIngestor.ingest_data(function=None)
    return Response(status_code=200)
