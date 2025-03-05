from weaviate.classes.config import Property, DataType, ReferenceProperty
import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv

def setup_weaviate_schema():
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

    # ✅ Create "Domains" collection (Top-level category)
    client.collections.create(
        "Domains",
        properties=[
            Property(name="name", data_type=DataType.TEXT, description="Name of the domain (e.g., Computer Science, Physics)"),
            Property(name="description", data_type=DataType.TEXT, description="Brief description of the domain"),
        ]
    )

    # ✅ Create "Subdomains" collection (Linked to Domain)
    client.collections.create(
        "Subdomains",
        properties=[
            Property(name="name", data_type=DataType.TEXT, description="Name of the subdomain (e.g., NLP, Quantum Mechanics)"),
            Property(name="description", data_type=DataType.TEXT, description="Brief description of the subdomain"),
            ReferenceProperty(name="belongs_to_domain", target_collection="Domains", description="Reference to the parent domain"),
        ]
    )

    # ✅ Create "Topics" collection (Linked to Subdomain)
    client.collections.create(
        "Topics",
        properties=[
            Property(name="name", data_type=DataType.TEXT, description="Name of the topic (e.g., Transformer Models, BERT)"),
            Property(name="description", data_type=DataType.TEXT, description="Brief description of the topic"),
            ReferenceProperty(name="belongs_to_subdomain", target_collection="Subdomains", description="Reference to the parent subdomain"),
        ]
    )
    client.close()  # Close the client to free up resources
