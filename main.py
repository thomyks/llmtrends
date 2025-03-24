# from fastapi import FastAPI
# from api.v1.endpoints.router import router as papers_router
# from api.v1.endpoints.router import router as dropdown_search_menu_router
# from services.database.weavite_client_cloud import client, close_weaviate_client
# # from services.database.weavite_client_local import client, close_weaviate_client
# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("FastAPI startup: Weaviate client is ready.")  
#     yield  # ✅ Keep the connection open while the app is running
#     print("FastAPI shutdown: Closing Weaviate client.")
#     close_weaviate_client()  # ✅ Close the connection when FastAPI stops

# # Initialize FastAPI 
# app = FastAPI()

# # Include versioned routers
# app.include_router(papers_router, prefix="/api/v1")
# app.include_router(dropdown_search_menu_router, prefix="/api/v1")



from fastapi import FastAPI
from api.v1.endpoints.router import router as papers_router
from api.v1.endpoints.router import router as dropdown_search_menu_router
from services.database.weavite_client_cloud import client, close_weaviate_client
# from services.database.weavite_client_local import client, close_weaviate_client
from contextlib import asynccontextmanager

# For AWS Lambda
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI startup: Weaviate client is ready.")  
    yield  # ✅ Keep the connection open while the app is running
    print("FastAPI shutdown: Closing Weaviate client.")
    close_weaviate_client()  # ✅ Close the connection when FastAPI stops

# Initialize FastAPI with lifespan context
app = FastAPI(lifespan=lifespan)

# Include versioned routers
app.include_router(papers_router, prefix="/api/v1")
app.include_router(dropdown_search_menu_router, prefix="/api/v1")

# Wrap with Mangum for AWS Lambda compatibility
handler = Mangum(app)

