from pydantic import BaseModel
from typing import List

from src.modules.shared.dto import FilterDTO


class ReportEntityRelationsDTO(BaseModel):
    docs_filter: FilterDTO
    root_entities: List[str]