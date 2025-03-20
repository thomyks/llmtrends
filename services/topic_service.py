from fastapi import HTTPException
from models.topic import TopicData  # Assuming you have a TopicData model
# from services.database.weavite_client_cloud import client
from services.database.weavite_client_local import client


def fetch_topics(include_vectors: bool, page: int, size: int):
    """
    Fetches topics from Weaviate with pagination.

    Args:
        include_vectors (bool): Whether to include vectors.
        page (int): Page number.
        size (int): Number of items per page.

    Returns:
        dict: Paginated list of topics with metadata.
    """
    try:
        # Get the "Topics" collection
        collection = client.collections.get("Topics")

        # Fetch all topics
        all_topics = [
            {
                "uuid": item.uuid,  # Unique ID of the object
                "properties": item.properties  # Topic data
            }
            for item in collection.iterator(include_vector=include_vectors)
        ]

        if not all_topics:
            raise HTTPException(status_code=404, detail="No topics found in collection.")

        # Apply pagination
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_topics = all_topics[start_idx:end_idx]

        return {
            "page": page,
            "size": size,
            "total_items": len(all_topics),
            "total_pages": (len(all_topics) + size - 1) // size,  # Ceiling division
            "topics": paginated_topics
        }
    
    except Exception as e:
        print(f"Fetch Error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=f"Fetch Error: {str(e)}")


def insert_topic(topic: TopicData):
    """
    Inserts a new topic into the Weaviate collection.

    Args:
        topic (TopicData): Topic data to insert.

    Returns:
        dict: Success message.
    """
    try:
        # Get the "Topics" collection
        collection = client.collections.get("Topics")
        
        # Convert topic data to dictionary
        topic_data = topic.dict()
        
        # Insert data into the collection
        collection.data.insert(topic_data)
        
        return {"message": "Topic inserted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion Error: {str(e)}")
