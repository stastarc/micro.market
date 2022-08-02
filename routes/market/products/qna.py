from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from database import scope, Product, Qna
from micro import auth_method, VerifyBody

router = APIRouter()

class qna_request(BaseModel):
    content: str

@router.get("/{product_id}/qnas")
def product_qnas(product_id: int, resp: Response, start: int = 0, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload
        
    with scope() as sess:
        res = [Qna.parse_qna_object_to_dict_short(qna) for qna in Qna.session_get_qnas(sess, product_id, start)]
        if not res:
            resp.status_code = 404
            return {"error": "There is no such result that matches your query."}
        return res

@router.get("/{product_id}/qnas/{qna_id}")
def product_qna(qna_id: int, resp: Response, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload
        
    with scope() as sess:
        res = Qna.session_get_specific_qna_full(sess, qna_id)
        if not res:
            resp.status_code = 404
            return {"error": "There is no such result that matches your query."}
        return res

@router.post("/{product_id}/qnas")
def create_qna(product_id: int, req : qna_request, resp: Response, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    if len(req.content) < 10 or len(req.content) > 5000:
        resp.status_code = 400
        return {"error": "Content length must be between 10 and 5000"}

    with scope() as sess:
        product = sess.query(Product).filter(Product.id == product_id).first()
        if not product:
            resp.status_code = 404
            return {"error": "Product not found"}

        qna = Qna.session_write_qna(sess, product_id, token.user_id, req.content)
        return {"qna": qna.id}