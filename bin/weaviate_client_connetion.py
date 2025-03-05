import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure

# Load environment variables from .env file 
from dotenv import load_dotenv
load_dotenv()

# Access credentials from environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

def get_weaviate_client() -> weaviate.Client:

    """
    Returns an instance of the Weaviate client.
    """
    # Load environment variables from .env file 
    # Access credentials from environment variables
    if weaviate_api_key:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=(weaviate_api_key), 
        )
        print("✅ Connected to Weaviate Cloud")
    else:
        client = weaviate.Client(url=weaviate_url)
  
    return client