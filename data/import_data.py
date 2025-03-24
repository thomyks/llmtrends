import json
from weaviate.classes.config import Property, DataType
import weaviate.classes as wvc
from services.database.weavite_client_cloud import client

# # Connect to local Weaviate instance using the correct method
# client = weaviate.connect_to_local(
#     host="127.0.0.1",  # Use a string to specify the host
#     port=8080,
#     grpc_port=50051,
# )


try:
    print("Weaviate connection ready:", client.is_ready())
    
    # Load the JSON file
    file_path = "/Users/tomasnagy/FastAPI/application/data/papers_sample.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Prepare data for insertion
    paper_objs = list()
    for i, d in enumerate(data):
        paper_objs.append(
            wvc.data.DataObject(
                properties={
                    "topic": d["topic"],
                    "paperId": i + 1,
                    "url": d["url"],
                    "date": d["date"] + "T00:00:00Z",
                    "title": d["title"],
                    "abstract": d["abstract"],
                    "domain": d["domain"],
                    "subdomain": d["subdomain"]
                },
                vector=json.loads(d["embeddings"]) if isinstance(d["embeddings"], str) else d["embeddings"]
            )
        )
    
    # Insert data into the LLMPapers collection
    llm_papers = client.collections.get("LLMPapers")
    llm_papers.data.insert_many(paper_objs)
    
    print("Data inserted into LLMPapers collection successfully!")

finally:
    # Close Weaviate connection
    client.close()
    print("Weaviate connection closed.")
