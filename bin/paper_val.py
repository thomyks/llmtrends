from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import date

class PaperBase(BaseModel):
    url: Optional[HttpUrl] = None
    date: Optional[date] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    topic: Optional[str] = None
    author: Optional[str] = None

class PaperCreate(PaperBase):
    paperId: str = Field(..., description="Unique ID of the paper")

class PaperOut(PaperBase):
    paperId: str
