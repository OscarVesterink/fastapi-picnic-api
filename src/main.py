import fastapi
from fastapi.middleware import cors

from src.core import config, openapi, logging
from src.database import crud as database_crud

views = ""

settings = config.get_settings()
PROXY_PORT = settings.PROXY_PORT
FRONTEND_PORT = settings.FRONTEND_PORT
ROOT_PATH = settings.ROOT_PATH

# Set up the loggers.
logger_settings = {
    "LOGGING_REQUESTS_FILE": settings.LOGGING_REQUESTS_FILE,
    "LOGGER_REQUESTS_NAME": settings.LOGGER_REQUESTS_NAME,
    "LOGGING_CONTROLLERS_FILE": settings.LOGGING_CONTROLLERS_FILE,
    "LOGGER_CONTROLLERS_NAME": settings.LOGGER_CONTROLLERS_NAME,
}
logging.setup_logging(logger_settings=logger_settings)

tag_metadata = openapi.get_openapi_tags_metadata()
app = fastapi.FastAPI(
    title="FaPi",
    version="0.0.1",
    swagger_ui_parameters={"operationsSorter": "method"},
    openapi_tags=tag_metadata,
    redoc_url=f"{ROOT_PATH}/redoc",
    docs_url=f"{ROOT_PATH}/docs",
    openapi_url=f"{ROOT_PATH}/openapi.json",
    debug=True,
)
prefix_router = fastapi.APIRouter(prefix=ROOT_PATH)
prefix_router.include_router(views.router)
app.include_router(prefix_router)

# Set up the database
database_crud.create_metadata()

# CORS middleware.
origins = [
    # Dev poorten
    f"http://127.0.0.1:{FRONTEND_PORT}",
    f"http://localhost:{FRONTEND_PORT}",
]
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)