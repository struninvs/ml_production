from typing import List

from schemas.base_schema import BaseSchema


class PredictTrendsRequest(BaseSchema):
    data: str

class PredictTrendsResponse(BaseSchema):
    trends_list: List[List[str]]