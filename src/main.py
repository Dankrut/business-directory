import logging
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

# Добавляем путь к корню проекта
sys.path.append(str(Path(__file__).parent.parent))

from src.api.activities import router as router_activities
from src.api.buildings import router as router_buildings
from src.api.organizations import router as router_organizations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Company Directory API",
    description="Справочник организаций, зданий и видов деятельности",
)

app.include_router(router_activities)
app.include_router(router_buildings)
app.include_router(router_organizations)

if __name__ == "__main__":
    logger.info("Starting Organization Catalog API...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
