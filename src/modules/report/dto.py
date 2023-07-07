from pydantic import BaseModel

from src.modules.shared.dto import FilterDTO


class ReportEntityRelationsDTO(BaseModel):
    docs_filter: FilterDTO
    root_entity: str