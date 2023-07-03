from fastapi import APIRouter

from .services import ReportServices
from src.modules.shared.dto import FilterDTO


report_router = APIRouter()


@report_router.post('/entity_frequency')
def get_entity_frequency(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_entity_frequency_data(docs_filter)
