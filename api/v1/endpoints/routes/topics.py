from fastapi import APIRouter, Query
from models.topic import TopicData  # Assuming this is the Pydantic model for Topic
from services.topic_service import insert_topic

# Initialize FastAPI router
router = APIRouter()


from services.topic_service import fetch_topics

# Initialize FastAPI router
router = APIRouter()

@router.get("/")
async def get_topics(
    include_vectors: bool = False, 
    page: int = Query(1, alias="page", ge=1), 
    size: int = Query(10, alias="size", ge=1, le=100)
):
    """
    API endpoint to fetch paginated topics from Weaviate.
    - page: Page number (default = 1).
    - size: Number of items per page (default = 10, max = 100).
    """
    return fetch_topics(include_vectors, page, size)



@router.post("/")
async def insert_topic_route(topic: TopicData):
    """
    API endpoint to insert a new topic into Weaviate.
    """
    return insert_topic(topic)
