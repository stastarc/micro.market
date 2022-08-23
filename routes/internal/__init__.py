from fastapi.routing import APIRouter
from . import search

router = APIRouter(prefix='/internal')

router.include_router(search.router)