from typing import Annotated
from fastapi import Depends, Header
from src.exceptions import ApiKeyInvalidHTTPException
from src.config import settings
from src.database import async_session_maker
from src.utils.db_manager import DBManager


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise ApiKeyInvalidHTTPException()
    return x_api_key


ApiKeyDep = Annotated[str, Depends(verify_api_key)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
