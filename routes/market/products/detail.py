from fastapi import APIRouter, Depends, Response
from database import Products, scope
from micro.auth import VerifyBody, auth_method

router = APIRouter()

@router.get("/{id}")
def product_detail(id: int, resp: Response, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    with scope() as sess:
        res = Products.session_get_specific_product_detail(sess, id)
        if not res:
            resp.status_code = 404
            return {"error": "No matching results"}
        return res