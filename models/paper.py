from pydantic import BaseModel, Field
from datetime import datetime

# Define the data model for the request payload
class PaperData(BaseModel):
    paperId: int
    url: str
    date: datetime = Field(..., description="Publication date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)")
    title: str
    abstract: str
    domain: str
    subdomain: str
    topic: str