from fastapi import APIRouter, Depends, Response
from database import Products, scope
from micro.auth import VerifyBody, auth_method

router = APIRouter()

@router.get("/{id}")
def product_detail(id: int, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    with scope() as sess:
        data = Products.session_get_detail(sess, id)
        
        if not data: return Response(status_code=404)

        return data