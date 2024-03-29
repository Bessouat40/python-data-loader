from fastapi import FastAPI, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from postgresIngestor import PostgresIngestor

app = FastAPI()

pgIngestor = PostgresIngestor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestDataRequest(BaseModel):
    path: str

@app.post('/ingest')
async def get_data(request: IngestDataRequest):
    pgIngestor.ingest_data(request.path)
    return Response(status_code=200)
