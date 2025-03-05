import pytest
from unittest.mock import MagicMock
from application.services.search_service import search_dropdown
from application.services.database.weavite_client_cloud import client

@pytest.fixture
def mock_weaviate():
    """Mock the Weaviate client."""
    client.query = MagicMock()

def test_search_dropdown_all(mock_weaviate):
    """Test BM25 search for both LLMPapers and Topics."""
    
    # Mock BM25 response for LLMPapers
    client.query.get.return_value.with_bm25.return_value.with_limit.return_value.do.return_value = {
        "data": {
            "Get": {
                "LLMPapers": [{"title": "Test Paper"}],
                "Topics": [{"name": "Test Topic"}]
            }
        }
    }

    result = search_dropdown("LLM", "All")

    assert "papers" in result["results"]
    assert "topics" in result["results"]
    assert len(result["results"]["papers"]) > 0
    assert len(result["results"]["topics"]) > 0

def test_search_dropdown_papers(mock_weaviate):
    """Test BM25 search for only LLMPapers."""
    
    client.query.get.return_value.with_bm25.return_value.with_limit.return_value.do.return_value = {
        "data": {
            "Get": {
                "LLMPapers": [{"title": "Test Paper"}]
            }
        }
    }

    result = search_dropdown("AI", "LLMPapers")

    assert "papers" in result["results"]
    assert len(result["results"]["papers"]) > 0

def test_search_dropdown_invalid_entity(mock_weaviate):
    """Test invalid entity type."""
    with pytest.raises(Exception) as e:
        search_dropdown("AI", "InvalidType")
    
    assert "Invalid entity_type" in str(e.value)
