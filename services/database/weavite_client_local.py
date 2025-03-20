import weaviate
from weaviate.classes.config import Property, DataType
import atexit

# Connect to local Weaviate instance using the correct method
client = weaviate.connect_to_local(
    host="127.0.0.1",  # Use a string to specify the host
    port=8080,
    grpc_port=50051,
    skip_init_checks=True
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
