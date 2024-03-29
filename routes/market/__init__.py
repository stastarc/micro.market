from fastapi.routing import APIRouter
from . import products, feed, search, recommended

router = APIRouter(prefix='/market')
router.include_router(products.router)
router.include_router(feed.router)
router.include_router(search.router)
router.include_router(recommended.router)