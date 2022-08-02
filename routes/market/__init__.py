from fastapi.routing import APIRouter
from . import products
from . import feed

router = APIRouter(prefix='/market')
router.include_router(products.router)
router.include_router(feed.router)