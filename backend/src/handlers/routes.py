from fastapi import Response, status
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

import handlers.health, handlers.ml
from schemas.predict_trends import PredictTrendsResponse


routes: list[BaseRoute] = [
    APIRoute(
        "/monitoring/status",
        handlers.health.liveness_probe,
        methods=["GET"],
        tags=["Monitoring"],
        summary="Service liveness probe",
        description="Service liveness probe",
        response_class=Response,
        status_code=status.HTTP_200_OK,
        include_in_schema=False,
        responses={
            200: {"description": "Success"},
            500: {"description": "Internal server error"},
        },
    ),
    APIRoute(
        "/monitoring/ready",
        handlers.health.readiness_probe,
        methods=["GET"],
        tags=["Monitoring"],
        summary="Service readiness probe",
        description="Service readiness probe",
        response_class=Response,
        status_code=status.HTTP_200_OK,
        include_in_schema=False,
        responses={
            200: {"description": "Success"},
            500: {"description": "Internal server error"},
        },
    ),
    APIRoute(
        "/api/v1/predict_trends",
        handlers.ml.predict_trends,
        methods=["GET"],
        tags=["ML"],
        summary="Predicts trends in User reviews",
        description="Predicts trends in User reviews",
        response_model=PredictTrendsResponse,
        status_code=status.HTTP_200_OK,
        include_in_schema=False,
        responses={
            200: {"description": "Success"},
            500: {"description": "Internal server error"},
        },
    )
]
