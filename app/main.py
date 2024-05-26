"""Start Application."""

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api_v1 import app as api_v1_router
from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION, APP_HOST, APP_PORT


def get_application() -> FastAPI:
    """Get app."""
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # application.add_middleware(GZipMiddleware, minimum_size=1000)
    application.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_v1_router, prefix=API_PREFIX)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=int(APP_PORT))
