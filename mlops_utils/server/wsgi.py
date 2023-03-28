from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mlops_utils.server.middlewares import *
from mlops_utils.server.exceptions import *


def get_application() -> FastAPI:
    # create application instance
    app = FastAPI()

    # add middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.add_middleware(TimeHeaderMiddleware)

    # exception-handlers
    app.add_exception_handler(HTTPException, http_error_handler)

    return app
