from weaviate.classes.config import Property, DataType
import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv

def insert_data_into_weaviate(collection_name, data):
    # Load environment variables
    load_dotenv()
    
    # Access credentials from environment variables
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    
    # Connect to Weaviate Cloud
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )
    
    # Get the specified collection
    collection = client.collections.get(collection_name)
    
    # Insert data into the collection
    collection.data.insert(data)
    
    # Close the client after inserting the data
    client.close()

# Example usage
if __name__ == "__main__":
    insert_data_into_weaviate("LLMPapers", {
        "paperId": 332,
        "url": "https://arxiv.org/abs/2302.00456",
        "date": "2023-02-15T00:00:00Z",
        "title": "A Comprehensive Survey on Large Language Models",
        "abstract": "This survey explores the rapid advancements in LLMs, including their architecture, training techniques, and real-world applications.",
        "domain": "Computer Science",
        "subdomain": "Machine Learning",
        "topic": "Survey on Large Language Models"
    })
