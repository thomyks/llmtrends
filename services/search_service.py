from fastapi import HTTPException
# from services.database.weavite_client_cloud import client
from services.database.weavite_client_local import client

def search_dropdown(query: str, entity_type: str):
    """
    Fetches search results for the dropdown menu using a direct query-based search.

    Args:
        query (str): Search term.
        entity_type (str): The type of entity to search for (LLMPapers, Topics).

    Returns:
        dict: Search results.
    """
    try:
        if entity_type == "All":
            # Fetch collections
            papers_collection = client.collections.get("LLMPapers")
            topics_collection = client.collections.get("Topics")

            # Perform a query-based search
            response_papers = papers_collection.query.fetch_objects().objects
            response_topics = topics_collection.query.fetch_objects().objects

            # Filter results based on search query
            filtered_papers = [paper for paper in response_papers if query.lower() in paper.properties.get("title", "").lower()]
            filtered_topics = [topic for topic in response_topics if query.lower() in topic.properties.get("name", "").lower()]

            results = {
                "papers": filtered_papers,
                "topics": filtered_topics,
            }

        elif entity_type in ["LLMPapers", "Topics"]:
            # Search within a specific entity type
            collection = client.collections.get(entity_type)
            response = collection.query.fetch_objects().objects

            property_name = "title" if entity_type == "LLMPapers" else "name"
            results = [item for item in response if query.lower() in item.properties.get(property_name, "").lower()]

        else:
            raise HTTPException(status_code=400, detail="Invalid entity_type. Choose 'LLMPapers' or 'Topics'.")

        return {"query": query, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")