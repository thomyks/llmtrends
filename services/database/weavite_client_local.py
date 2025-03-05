import weaviate
from weaviate.classes.config import Property, DataType

# Connect to local Weaviate instance using the correct method
client = weaviate.connect_to_local(
    host="127.0.0.1",  # Use a string to specify the host
    port=8080,
    grpc_port=50051,
)

print(client.is_ready())

# Only close Weaviate when explicitly called
def close_weaviate_client():
    global client
    if client is not None:
        client.close()
        print("✅ Weaviate connection closed.")


