import logging
import uvicorn

from fastapi import FastAPI, APIRouter

from qitc.backend.db import db_init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/qitc")

# Список роутеров

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    db_init()
    uvicorn.run(app, host="0.0.0.0", port=8000)