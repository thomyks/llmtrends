# import weaviate
# from weaviate.classes.config import Property, DataType
# import atexit

# # Connect to local Weaviate instance using the correct method
# client = weaviate.connect_to_local(
#     # host="127.0.0.1", 
#     host="weaviate",  # 👈 this is the container name

#     # host="localhost",  # 👈 this is the container name
#  # Use a string to specify the host
#     port=8080,
#     grpc_port=50051,
#     skip_init_checks=True
# )

# print("✅ Weaviate is ready:", client.is_ready())
# print("✅ Weaviate connection established.")
# print("✅ Weaviate schema is ready:", client.get_meta())

# def close_weaviate_client():
#     global client
#     if client is not None:
#         client.close()
#         print("✅ Weaviate connection closed.")
# atexit.register(close_weaviate_client)




import weaviate
import time
import atexit
from weaviate.exceptions import WeaviateStartUpError

client = None

# Retry logic — give Weaviate time to boot
for attempt in range(10):
    try:
        client = weaviate.connect_to_local(
            host="localhost",  # Docker container name
            port=8080,
            grpc_port=50051,
            skip_init_checks=True
        )
        if client.is_ready():
            print("✅ Connected to Weaviate")
            break
    except Exception as e:
        print(f"⏳ Waiting for Weaviate... attempt {attempt+1}/10 | Error: {e}")
        time.sleep(3)
else:
    raise WeaviateStartUpError("❌ Could not connect to Weaviate after 10 attempts.")

# Optional: log meta
try:
    print("ℹ️ Meta:", client.get_meta())
except Exception:
    print("⚠️ Could not get meta info.")

# Cleanup
def close_weaviate_client():
    if client:
        client.close()
        print("🛑 Weaviate client closed.")

atexit.register(close_weaviate_client)

