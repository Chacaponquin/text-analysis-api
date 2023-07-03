from pydantic import BaseModel

class FindEntity(BaseModel):
   entity_name: str