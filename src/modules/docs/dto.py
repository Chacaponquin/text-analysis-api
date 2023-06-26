from pydantic import BaseModel


class FindDocDTO(BaseModel):
   entities: list[str]
   categories: list[str]
   document_title: str