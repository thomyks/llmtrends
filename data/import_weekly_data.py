import json
import weaviate
from weaviate.classes.config import Property, DataType
import weaviate.classes as wvc
from datetime import datetime

# Connect to local Weaviate instance
client = weaviate.connect_to_local(
    host="127.0.0.1",  # Use a string to specify the host
    port=8080,
    grpc_port=50051,
)

try:
    print("Weaviate connection ready:", client.is_ready())

    # Load the JSONL file
    file_path = "/Users/tomasnagy/FastAPI/application/data/updated_2025-03-17_merged.jsonl"
    with open(file_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    # Function to format dates in RFC3339 format
    def format_date(date_str):
        """Ensure date is in RFC3339 format, fallback to 1970-01-01 if missing."""
        try:
            if not date_str or date_str.strip() == "":
                return "1970-01-01T00:00:00Z"  # Default fallback
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%dT00:00:00Z")
        except ValueError:
            return "1970-01-01T00:00:00Z"

    # Function to ensure embeddings are valid
    def process_embedding(embedding):
        """Ensure embedding is a valid 384-dimensional list."""
        if isinstance(embedding, str):
            try:
                embedding = json.loads(embedding)  # Convert string to list
            except json.JSONDecodeError:
                return [0.0] * 384  # Return zero vector if JSON conversion fails
        if not isinstance(embedding, list) or len(embedding) != 384:
            return [0.0] * 384  # Default to zero vector if incorrect size
        return embedding

    # Prepare data for insertion
    paper_objs = []
    for i, d in enumerate(data):
        paper_objs.append(
            wvc.data.DataObject(
                properties={
                    "paperId": d.get("id", 0),  # Default: 0 if missing
                    "topic": d.get("assigned_concept", ""),  # Use assigned topic
                    "title": d.get("title", ""),  # Default: empty string
                    "abstract": d.get("abstract", ""),  # Default: empty string
                    "authors": d.get("authors", ""),  # Default: empty string
                    "categories": d.get("categories", ""),  # Default: empty string
                    "url": d.get("comments", ""),  # Store metadata like project page
                    "date": format_date(d.get("update_date", "")),  # Use update_date
                },
                vector=process_embedding(d.get("embedding"))  # ✅ Uses embedding
            )
        )

    # Insert data into the LLMPapers collection
    if paper_objs:
        llm_papers = client.collections.get("LLMPapers")
        llm_papers.data.insert_many(paper_objs)
        print("✅ Data inserted into LLMPapers collection successfully!")
    else:
        print("⚠️ No valid records found to insert.")

finally:
    # Close Weaviate connection
    client.close()
    print("Weaviate connection closed.")
