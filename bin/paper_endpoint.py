from fastapi import APIRouter, Depends, HTTPException
from weaviate import Client as WeaviateClient
from uuid import uuid4
from weaviate_client_connetion import get_weaviate_client
from paper_val import PaperCreate, PaperOut

router = APIRouter()

@router.post("/", response_model=PaperOut)
def create_paper(
    paper: PaperCreate,
    client: WeaviateClient = Depends(get_weaviate_client),
):
    """
    Create a new Paper in Weaviate.
    """
    # We'll let Weaviate store it with a randomly generated UUID.
    paper_uuid = str(uuid4())

    obj_data = {
        "paperId": paper.paperId,
        "url": paper.url,
        "date": paper.date.isoformat() if paper.date else None,
        "title": paper.title,
        "abstract": paper.abstract,
        "domain": paper.domain,
        "subdomain": paper.subdomain,
        "topic": paper.topic,
        "author": paper.author,
    }

    try:
        client.data_object.create(
            data_object=obj_data,
            class_name="Paper",
            uuid=paper_uuid
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PaperOut(**obj_data)
