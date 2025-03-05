from fastapi import APIRouter
from api.v1.endpoints.routes.papers import router as papers_router
from api.v1.endpoints.routes.dropdown_search_menu import router as dropdown_search_menu_router
from api.v1.endpoints.routes.topics import router as topics_router

router = APIRouter()
router.include_router(papers_router, prefix="/papers", tags=["Papers"])
router.include_router(topics_router, prefix="/topics", tags=["Topics"])
router.include_router(dropdown_search_menu_router, prefix="/search-dropdown", tags=["Dropdown Search Menu"])