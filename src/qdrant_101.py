from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import numpy as np

client = QdrantClient("http://localhost:6333")

# Create a collection with cosine distance
client.recreate_collection(
    collection_name="companies",
    vectors_config=VectorParams(size=3, distance=Distance.COSINE),
)

# Dummy normalized vectors
vectors = np.array([
    [1.0, 0.0, 0.0],  # Apple
    [0.9, 0.1, 0.0],  # Google-ish
    [0.0, 1.0, 0.0],  # Banana
])

# Insert points
client.upsert(
    collection_name="companies",
    points=[
        {"id": i, "vector": vec.tolist()} for i, vec in enumerate(vectors)
    ]
)

# Search
query = [1.0, 0.1, 0.0]  # same direction as Apple
hits = client.search(collection_name="companies", query_vector=query, limit=2)

for hit in hits:
    print(f"ID: {hit.id}, Score: {hit.score}")
