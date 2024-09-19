from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


async def liveness_probe(_: Request) -> JSONResponse:
    return JSONResponse(jsonable_encoder({"alive": True}), status_code = status.HTTP_200_OK)


async def readiness_probe(_: Request) -> JSONResponse:
    # TODO: check connections readiness
    return JSONResponse(jsonable_encoder({"ready": True}), status_code = status.HTTP_200_OK)
