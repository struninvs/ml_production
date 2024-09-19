from typing import Union
import requests

from core.logger import JSONLogger
from core.definitions import (
    BACKEND_HOST,
    BACKEND_PORT
)
from services.trends_indicator.schemas.predict_trends import PredictTrendsRequest


logger = JSONLogger(__name__)

def predict_trends(data: str) -> requests.models.Response:
    global logger
    request_model: PredictTrendsRequest

    request_model = PredictTrendsRequest(
        data = data
    )

    url = f"{BACKEND_HOST}:{BACKEND_PORT}/api/v1/predict_trends"
    response = requests.get(url, json=request_model.model_dump())

    return response
