from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-large"
COLLECTION_NAME = "company_embeddings"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient("http://localhost:6333")

def query_qdrant(query: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = response.data[0].embedding

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5,
    )
    for result in results:
        print(f"{result.payload['company_name']}: {result.score}")
    
    return results
    
        
