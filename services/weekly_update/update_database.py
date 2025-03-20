# Current problem: the date is not working properly. 
import json
import weaviate
from weaviate.classes.config import Property, DataType
import weaviate.classes as wvc
from datetime import datetime
import os
from config import WEEKLY_DATA_PATH

def insert_papers_into_weaviate(file_path):
    """
    Reads a JSONL file, processes the data, and inserts it into the Weaviate database.
    
    Args:
        file_path (str): Path to the JSONL file containing paper data.
    """
    # Connect to local Weaviate instance
    client = weaviate.connect_to_local(
        host="127.0.0.1",  # Use a string to specify the host
        port=8080,
        grpc_port=50051,
    )

    try:
        print("Weaviate connection ready:", client.is_ready())

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

        # Load the JSONL file
        with open(file_path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]

        # Prepare data for insertion
        paper_objs = []
        for d in data:
            paper_id = d.get("id", "")  # Ensure we have a valid paper ID
            arxiv_url = f"https://arxiv.org/pdf/{paper_id}.pdf" if paper_id else ""
            
            paper_objs.append(
                wvc.data.DataObject(
                    properties={
                        "paperId": paper_id,
                        "topic": d.get("assigned_concept", ""),
                        "title": d.get("title", ""),
                        "abstract": d.get("abstract", ""),
                        "authors": d.get("authors", ""),
                        "categories": d.get("categories", ""),
                        "url": arxiv_url,
                        "date": format_date(d.get("update_date", "")),
                    },
                    vector=process_embedding(d.get("embedding"))
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

# Example usage:
# today = datetime.now()
# base_input_folder = os.path.join(WEEKLY_DATA_PATH, "output")
# input_filename = f"{today.strftime('%Y-%m-%d')}_merged_with_topics.jsonl" 
# updated_data_path = os.path.join(base_input_folder, input_filename)
# print(updated_data_path)
# insert_papers_into_weaviate(updated_data_path)