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
    # Get embedding
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = response.data[0].embedding

    # --- HNSW search (approximate) ---
    hnsw_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5
    )
    
    print("\n🔍 HNSW (Approximate) Results:")
    for r in hnsw_results:
        print(f"[HNSW] {r.payload['company_name']} (Index: {r.payload['index']}, Score: {r.score:.4f})")

    # --- Exact cosine search ---
    exact_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5,
        search_params={"exact": True}
    )
    
    print("\n🧠 Exact Cosine (Brute-force) Results:")
    for r in exact_results:
        print(f"[Exact] {r.payload['company_name']} (Index: {r.payload['index']}, Score: {r.score:.4f})")

    return {
        "hnsw": hnsw_results,
        "exact": exact_results
    }
