from os import listdir, environ
from dotenv import load_dotenv, find_dotenv
import warnings
from elasticsearch import Elasticsearch
import base64

load_dotenv(find_dotenv())

ELASTIC_PORT=environ.get("ELASTIC_PORT")
ELASTIC_HOST=environ.get("ELASTIC_HOST")
DATA_FOLDER="/data/elastic"

class ElasticIngestor:

    def __init__(self) :
        self.client = Elasticsearch(f"http://{ELASTIC_HOST}:{ELASTIC_PORT}")
        self.nbr_insert = 0

    @staticmethod
    def read_document(file_path):
        with open(file_path, "rb") as f:
            document_content = f.read()
            document_base64 = base64.b64encode(document_content).decode("utf-8")
            return document_base64
        
    @staticmethod
    def get_data_list(path) :
        data_list = listdir(path)
        document_list = [path + "/" + data for data in data_list]
        return document_list

    def get_last_document_id(self):
        if not self.client.indices.exists(index="document"): return 0
        search_body = {
            "query": {
                "match_all": {}
            },
            "sort": [{"document_id": {"order": "desc"}}],
            "size": 1
        }
        response = self.client.search(index="document", body=search_body)
        
        if response["hits"]["total"]["value"] > 0:
            last_image = response["hits"]["hits"][0]
            last_image_id = last_image["_source"]["document_id"]
            return last_image_id
        else:
            return 0

            
    def index_document(self, document_path, document_id):
        try :
            document_embedding = self.read_document(document_path)
            doc = {
                "document_id": document_id,
                "document_embedding": document_embedding,
                "extension": document_path.split('/')[-1].split(".")[-1]
            }
            self.client.index(index="document", id=document_id, body=doc)
            self.nbr_insert += 1
        except Exception as e :
            warnings.warn(f"Error occured : {e}")

    def ingest_data(self):
        print("---------- Start Data Ingestion ----------")
        self.nbr_insert = 0
        last_id = self.get_last_document_id()
        documents = self.get_data_list(DATA_FOLDER)
        print(f'\nWe found {len(documents)} documents to process\n')
        print("-" * 25)
        print('\n')
        [self.index_document(doc, idx + last_id) for idx, doc in enumerate(documents)]
        print('\n')
        print("-" * 25)
        print('\n')
        print(f"Total : {self.nbr_insert} documents inserted\n")
        print("---------- End Data Ingestion ----------")
