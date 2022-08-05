from fastapi import APIRouter, Depends
from database import scope, Feeds

from micro.auth import VerifyBody, auth_method

router = APIRouter(prefix="/feed")

@router.get("/")
def market_main_feed(token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    with scope() as sess:
        return Feeds.session_get_feed(sess)
