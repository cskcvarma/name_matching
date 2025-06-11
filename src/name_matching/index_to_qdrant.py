import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

COLLECTION_NAME = "company_embeddings"
EMBEDDINGS_PATH = "data/company_embeddings.json"
EMBEDDING_DIM = 3072


def load_embeddings_into_qdrant():
    with open(EMBEDDINGS_PATH, "r") as f:
        embedding_data = json.load(f)
        
    qdrant = QdrantClient("http://localhost:6333")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )

    points = [
        {"id": item["idx"], "vector": item["embedding"], 
        "payload": {"company_name": item["company_name"],"index": item["idx"]}}
        for item in embedding_data
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Loaded {len(embedding_data)} embeddings into Qdrant")
    return "DONE"