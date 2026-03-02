from fastapi import APIRouter, Query

from .schemas import (
    CanadaProvinceUniversitiesResponse,
    RegionCountryUniversitiesResponse,
    RegionItemsResponse,
    SearchResponse,
    StringItemsResponse,
    UniversityRead,
    UsStateUniversitiesResponse,
)


router = APIRouter()


def _empty_university_items() -> list[UniversityRead]:
    return []


@router.get("/regions", response_model=StringItemsResponse)
def get_regions() -> StringItemsResponse:
    return StringItemsResponse(items=["north-america", "europe", "asia-pacific"])


@router.get("/regions/{region}/countries", response_model=RegionItemsResponse)
def get_region_countries(region: str) -> RegionItemsResponse:
    return RegionItemsResponse(region=region, items=[])


@router.get(
    "/regions/{region}/countries/{country}/universities",
    response_model=RegionCountryUniversitiesResponse,
)
def get_universities_by_country(region: str, country: str) -> RegionCountryUniversitiesResponse:
    return RegionCountryUniversitiesResponse(
        region=region,
        country=country,
        items=_empty_university_items(),
    )


@router.get(
    "/regions/north-america/us/{state}/universities",
    response_model=UsStateUniversitiesResponse,
)
def get_us_state_universities(state: str) -> UsStateUniversitiesResponse:
    return UsStateUniversitiesResponse(
        region="north-america",
        country="us",
        state=state,
        items=_empty_university_items(),
    )


@router.get(
    "/regions/north-america/canada/{province}/universities",
    response_model=CanadaProvinceUniversitiesResponse,
)
def get_canada_province_universities(province: str) -> CanadaProvinceUniversitiesResponse:
    return CanadaProvinceUniversitiesResponse(
        region="north-america",
        country="canada",
        province=province,
        items=_empty_university_items(),
    )


@router.get("/search", response_model=SearchResponse)
def search_universities(name: str = Query(min_length=1)) -> SearchResponse:
    return SearchResponse(query=name, items=_empty_university_items())
