from fastapi.routing import APIRouter
from . import qna
from . import detail
from . import reviews

router = APIRouter(prefix='/products')
router.include_router(qna.router)
router.include_router(detail.router)
router.include_router(reviews.router)