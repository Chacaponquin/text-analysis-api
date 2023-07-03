from fastapi import APIRouter

from .services import ReportServices
from src.modules.shared.dto import FilterDTO


report_router = APIRouter()


@report_router.post('/entity_frequency')
def get_entity_frequency(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_entity_frequency_data(docs_filter)


@report_router.post('/category_frequency')
def get_category_frequency(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_category_frequence_data(docs_filter)

@report_router.post('/entity_over_time')
def get_entity_over_time(docs_filter: FilterDTO):
    report_services = ReportServices()
    return report_services.get_entity_over_time_data(docs_filter)
