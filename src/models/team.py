from pydantic import BaseModel
from typing import Optional

class Team(BaseModel):
    name: str
    endpoint: str
    api_key: str
