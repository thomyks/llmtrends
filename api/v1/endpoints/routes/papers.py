from fastapi import APIRouter, Query, HTTPException
from services.paper_service import fetch_papers
from services.paper_service import insert_paper
from services.paper_service import delete_paper
from models.paper import PaperData  


# Initialize FastAPI router
router = APIRouter()

@router.get("/")
async def get_papers(
    collection_name: str, 
    include_vectors: bool = False, 
    page: int = Query(1, alias="page", ge=1), 
    size: int = Query(10, alias="size", ge=1, le=100)
):
    """
    API endpoint to fetch paginated papers from a Weaviate collection.
    - page: Page number (default = 1).
    - size: Number of items per page (default = 10, max = 100).
    """
    return fetch_papers(collection_name, include_vectors, page, size)


@router.post("/")
async def insert_paper_route(collection_name: str, paper: PaperData):
    """
    API endpoint to insert a new paper into Weaviate.
    """
    return insert_paper(collection_name, paper)


@router.delete("/{paper_id}")
async def delete_paper_route(collection_name: str, paper_id: int):
    """
    API endpoint to delete a paper from Weaviate using paperId.
    """
    try:
        result = delete_paper(collection_name, paper_id)  # Avoid naming conflict
        if not result:
            raise HTTPException(status_code=404, detail="Paper not found")
        return {"message": "Paper deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# from fastapi import FastAPI, HTTPException, Query
# from pydantic import BaseModel, Field
# from datetime import datetime
# import weaviate
# from weaviate.classes.init import Auth
# import os
# from dotenv import load_dotenv
# from fastapi import APIRouter
# from services.database.weavite_client import client
# from models.paper import PaperData  



# # Initialize FastAPI app
# router = APIRouter()

# @router.post("/")
# async def insert_paper(collection_name: str, paper: PaperData):
#     try:
#         # Get the specified collection
#         collection = client.collections.get(collection_name)
        
#         # Convert datetime to string for storage
#         paper_data = paper.dict()
#         paper_data["date"] = paper.date.isoformat()
        
#         # Insert data into the collection
#         collection.data.insert(paper_data)
        
#         return {"message": "Data inserted successfully"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# Return all the Papers
# @app.get("/papers/")
# def get_papers(collection_name: str, include_vectors: bool = False):
#     try:
#         # Get the specified collection
#         collection = client.collections.get(collection_name)

#         # Iterate through all objects in the collection
#         papers = []
#         for item in collection.iterator(include_vector=include_vectors):
#             papers.append({
#                 "uuid": item.uuid,  # Unique ID of the object
#                 "properties": item.properties  # Paper data
#             })

#         if not papers:
#             raise ValueError(f"No objects found in collection: {collection_name}")

#         return {"papers": papers}
    
#     except Exception as e:
#         print(f"Fetch Error: {e}")  # Log the error for debugging
#         raise HTTPException(status_code=500, detail=f"Fetch Error: {str(e)}")
    


# @router.get("/")
# async def get_papers(
#     collection_name: str, 
#     include_vectors: bool = False, 
#     page: int = Query(1, alias="page", ge=1), 
#     size: int = Query(10, alias="size", ge=1, le=100)
# ):
#     """
#     Fetches papers from a given collection with pagination.
#     - page: Page number (default = 1).
#     - size: Number of items per page (default = 10, max = 100).
#     """
#     try:
#         # Get the specified collection
#         collection = client.collections.get(collection_name)

#         # Fetch all objects in the collection
#         all_papers = [
#             {
#                 "uuid": item.uuid,  # Unique ID of the object
#                 "properties": item.properties  # Paper data
#             }
#             for item in collection.iterator(include_vector=include_vectors)
#         ]

#         if not all_papers:
#             raise HTTPException(status_code=404, detail=f"No papers found in collection: {collection_name}")

#         # Apply pagination
#         start_idx = (page - 1) * size
#         end_idx = start_idx + size
#         paginated_papers = all_papers[start_idx:end_idx]

#         return {
#             "page": page,
#             "size": size,
#             "total_items": len(all_papers),
#             "total_pages": (len(all_papers) + size - 1) // size,  # Ceiling division
#             "papers": paginated_papers
#         }
    
#     except Exception as e:
#         print(f"Fetch Error: {e}")  # Log the error for debugging
#         raise HTTPException(status_code=500, detail=f"Fetch Error: {str(e)}")

#     # finally:
#     #     client.close()  # Ensure proper resource cleanup
