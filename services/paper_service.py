from fastapi import APIRouter, HTTPException, Query
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter
from dotenv import load_dotenv
from models.paper import PaperData  
from fastapi import HTTPException
from services.database.weavite_client_cloud import client
# from services.database.weavite_client_local import client


def fetch_papers(collection_name: str, include_vectors: bool, page: int, size: int):
    """
    Fetches papers from a given Weaviate collection with pagination.

    Args:
        collection_name (str): Name of the Weaviate collection.
        include_vectors (bool): Whether to include vectors.
        page (int): Page number.
        size (int): Number of items per page.

    Returns:
        dict: Paginated list of papers with metadata.
    """
    try:
        # Get the specified collection
        collection = client.collections.get(collection_name)

        # Fetch all objects in the collection
        all_papers = [
            {
                "uuid": item.uuid,  # Unique ID of the object
                "properties": item.properties  # Paper data
            }
            for item in collection.iterator(include_vector=include_vectors)
        ]

        if not all_papers:
            raise HTTPException(status_code=404, detail=f"No papers found in collection: {collection_name}")

        # Apply pagination
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_papers = all_papers[start_idx:end_idx]

        return {
            "page": page,
            "size": size,
            "total_items": len(all_papers),
            "total_pages": (len(all_papers) + size - 1) // size,  # Ceiling division
            "papers": paginated_papers
        }
    
    except Exception as e:
        print(f"Fetch Error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=f"Fetch Error: {str(e)}")



def insert_paper(collection_name: str, paper: PaperData):
    """
    Inserts a new paper into the Weaviate collection.

    Args:
        collection_name (str): Name of the Weaviate collection.
        paper (PaperData): Paper data to insert.

    Returns:
        dict: Success message.
    """
    try:
        # Get the specified collection
        collection = client.collections.get(collection_name)
        
        # Convert datetime to string for storage
        paper_data = paper.dict()
        paper_data["date"] = paper.date.isoformat()
        
        # Insert data into the collection
        collection.data.insert(paper_data)
        
        return {"message": "Data inserted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion Error: {str(e)}")
    

def delete_paper(collection_name: str, paper_id: int):
    """
    Deletes a paper from the Weaviate collection using paperId.
    """
    try:
        collection = client.collections.get(collection_name)
        
        # Use Weaviate's delete_many with a filter on paperId
        result = collection.data.delete_many(
            where=Filter.by_property("paperId").equal(paper_id)
        )
        
        # Correctly access the matches attribute from DeleteManyReturn object
        if not result or not hasattr(result, "matches") or result.matches == 0:
            raise HTTPException(status_code=404, detail=f"Paper with paperId {paper_id} not found")
        
        return {"message": "Paper deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion Error: {str(e)}")