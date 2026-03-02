from pydantic import BaseModel, ConfigDict, HttpUrl


class UniversityBase(BaseModel):
    official_name: str
    english_name: str | None = None
    region: str
    country: str
    website: HttpUrl


class UniversityRead(UniversityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StringItemsResponse(BaseModel):
    items: list[str]


class RegionItemsResponse(BaseModel):
    region: str
    items: list[str]


class RegionCountryUniversitiesResponse(BaseModel):
    region: str
    country: str
    items: list[UniversityRead]


class UsStateUniversitiesResponse(BaseModel):
    region: str
    country: str
    state: str
    items: list[UniversityRead]


class CanadaProvinceUniversitiesResponse(BaseModel):
    region: str
    country: str
    province: str
    items: list[UniversityRead]


class SearchResponse(BaseModel):
    query: str
    items: list[UniversityRead]


class HealthcheckResponse(BaseModel):
    status: str
    service: str
