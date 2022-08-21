from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from database import scope, Recommended

from micro import VerifyBody, auth_method

router = APIRouter(prefix="/recommended")

@router.get("/{id}")
def get(
    id: int = Query(default=1),
    token: VerifyBody = Depends(auth_method)):
    
    if not token.success:
        return token.payload

    with scope() as sess:
        data = Recommended.session_get_data(sess, id)

    if not data:
        return Response(status_code=404)

    with scope() as sess:
        return {
            'recommended': data
        }