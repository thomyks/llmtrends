from pydantic import BaseModel

class TopicData(BaseModel):
    name: str
    description: str