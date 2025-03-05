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

# from fastapi import HTTPException
# from services.database.weavite_client import client

# def search_dropdown(query: str, entity_type: str):
#     """
#     Fetches search results for the dropdown menu.
    
#     Args:
#         query (str): Search term.
#         entity_type (str): The type of entity to search for (Paper, Topic, Subdomain, Domain).

#     Returns:
#         dict: Search results.
#     """
#     try:
#         if entity_type == "All":
#             # Search across all entity types
#             response_paper = client.query.get("Paper", ["title"]).with_hybrid(query).with_limit(5).do()
#             response_topic = client.query.get("Topic", ["name"]).with_hybrid(query).with_limit(5).do()
#             response_subdomain = client.query.get("Subdomain", ["name"]).with_hybrid(query).with_limit(5).do()
#             response_domain = client.query.get("Domain", ["name"]).with_hybrid(query).with_limit(5).do()

#             results = {
#                 "papers": response_paper["data"]["Get"]["Paper"],
#                 "topics": response_topic["data"]["Get"]["Topic"],
#                 "subdomains": response_subdomain["data"]["Get"]["Subdomain"],
#                 "domains": response_domain["data"]["Get"]["Domain"]
#             }
        
#         else:
#             # Search for a specific entity type
#             response = client.query.get(entity_type, ["name" if entity_type != "Paper" else "title"]).with_hybrid(query).with_limit(10).do()
#             results = response["data"]["Get"].get(entity_type, [])

#         return {"query": query, "results": results}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")