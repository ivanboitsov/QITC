import logging
import uvicorn
import asyncio

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from db.db_init import db_init

from routers.task_router import task_router
from routers.course_router import course_router
from routers.applicatoin_router import application_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/qitc")

router.include_router(application_router)
router.include_router(course_router)
router.include_router(task_router)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)