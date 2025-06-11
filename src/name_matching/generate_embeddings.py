import pandas as pd
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
EMBEDDING_MODEL = "text-embedding-3-large"
CSV_PATH = "data/updated_test_companies.csv"
OUTPUT_PATH = "data/company_embeddings.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_and_save_embeddings():
    df = pd.read_csv(CSV_PATH)
    output_data = []

    for idx, row in df.iterrows():
        company_name = row["company_name"]
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=company_name,
        )
        embedding = response.data[0].embedding
        output_data.append({"company_name": company_name,
     "embedding": embedding, 
     "idx": idx})
        print(f"Processed {idx + 1}/{len(df)}: {company_name}")
        time.sleep(0.1)
    
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output_data, f)

    print(f"Processed {len(df)} companies. Saved to {OUTPUT_PATH}")
    return "DONE"
    
