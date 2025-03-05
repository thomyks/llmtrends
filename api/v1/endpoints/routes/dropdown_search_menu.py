# from fastapi import APIRouter, Query
# from services.search_service import search_dropdown

# # Initialize FastAPI router
# router = APIRouter()

# @router.get("/")
# def search_dropdown_route(
#     query: str = Query(..., description="Search query"),
#     entity_type: str = Query("All", description="Filter by type: Paper, Topic, Subdomain, Domain")
# ):
#     """
#     API endpoint for dropdown search across different entity types.
#     """
#     return search_dropdown(query, entity_type)


from fastapi import APIRouter, Query
from services.search_service import search_dropdown

router = APIRouter()

# @router.get("/", operation_id="dropdown_search_data")
# async def search_dropdown_route(query: str = Query(...), entity_type: str = Query("All")):
#     """Dropdown search for Papers and Topics."""
#     return search_dropdown(query, entity_type)


@router.get("/")
async def search_dropdown_route(query: str = Query(...), entity_type: str = Query("All")):
    """Dropdown search for Papers and Topics."""
    return search_dropdown(query, entity_type)
