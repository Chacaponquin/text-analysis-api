from pydantic import BaseModel

class FindCategory(BaseModel):
   category_name: str