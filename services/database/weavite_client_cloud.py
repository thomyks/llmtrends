# connection to Weaviate Cloud
from weaviate.classes.config import Property, DataType
import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
import atexit


# Load environment variables
load_dotenv()

# Access credentials from environment variables
WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY = os.environ["WEAVIATE_API_KEY"]

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)

print("✅ Weaviate is ready:", client.is_ready())
print("✅ Weaviate connection established.")
print("✅ Weaviate schema is ready:", client.get_meta())

def close_weaviate_client():
    global client
    if client is not None:
        client.close()
        print("✅ Weaviate connection closed.")
atexit.register(close_weaviate_client)


# # Only close Weaviate when explicitly called
# def close_weaviate_client():
#     global client
#     if client is not None:
#         client.close()
#         print("✅ Weaviate connection closed.")



