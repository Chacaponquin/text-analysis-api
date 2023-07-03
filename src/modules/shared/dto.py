from pydantic import BaseModel
from typing import List

class FilterDTO(BaseModel):
   entities: List[str]
   categories: List[str]
   document_title: str
   year_init: int
   year_finish: int