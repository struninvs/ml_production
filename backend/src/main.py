from contextlib import asynccontextmanager
import functools
from typing import AsyncGenerator, Any, Union

import json
import pickle
import uvicorn
import uvloop
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


from core.definitions import DATA_DIR, MODEL_DIR
from handlers.routes import routes
from core.settings import Settings
from core.logger import JSONLogger

logger = JSONLogger(__name__)
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    
    logger.info("Starting up...")
    await register_app_dependencies(app)
    logger.info("Start is complete!")
    
    yield
    
    logger.info("Shutdown is complete!")


async def validation_error_handler(request: Request, exception: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": exception.errors(),
            "body": exception.body
        }
    )


async def exception_handler(_: Request, __: Exception) -> Response:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def create_app()-> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        lifespan = lifespan,
        debug=settings.DEBUG,
        exception_handlers={
            RequestValidationError: validation_error_handler,
            Exception: exception_handler,
        },
    )
    app.include_router(router=APIRouter(routes=routes))
    return app


async def run_server(entrypoint: Union[str, FastAPI], port: int) -> None:
    config = uvicorn.Config(
        entrypoint,
        host=str(settings.APP_HOST),
        port=port,
        log_level=settings.LOGLEVEL.lower(),
    )
    srv = uvicorn.Server(config=config)

    logger.info("Server is running on %s:%s", settings.APP_HOST, port)

    try:
        await srv.serve()
    except Exception as exc: 
        logger.exception(exc)


def event_shutdown()-> None:
    raise Exception("Error")


async def register_app_dependencies(app: FastAPI) -> None:
    
    app.state.server_logger = logger
    with open(MODEL_DIR / 'model.pkl', 'rb') as f:
        app.state.model = pickle.load(f)
    with open(DATA_DIR / 'mapping_backend.json', 'r') as f:
        app.state.mapping = json.load(f)

    app.add_event_handler(event_type="shutdown", func=functools.partial(event_shutdown))


async def main() -> None:
    uvloop.install()

    app = create_app()

    await run_server(app, settings.APP_PORT)