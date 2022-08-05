from datetime import datetime
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from database import scope, Product, Qna
from micro import auth_method, VerifyBody

router = APIRouter()

class QnARequest(BaseModel):
    content: str

@router.get("/{product_id}/qnas")
def product_qnas(product_id: int, offset: int = 0, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload
    
    with scope() as sess:
        if not Product.session_exists(sess, product_id):
            return Response(status_code=404)

        return Qna.session_get_shorts(sess, product_id, offset=offset)

@router.post("/{product_id}/qnas")
def create_qna(product_id: int, req: QnARequest, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    if not 10 <= len(req.content) <= 1000:
        return Response(status_code=400)

    with scope() as sess:
        if not Product.session_exists(sess, product_id):
            return Response(status_code=404)

        qna = Qna.session_add(sess, product_id, token.payload.id, req.content)  # type: ignore

        return {
            'qna': {
                'id': qna.id,
            }
        }