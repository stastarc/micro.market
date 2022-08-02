from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from database import scope, Rating
from micro import auth_method, VerifyBody


router = APIRouter()

@router.get("/{product_id}/reviews")
def product_desc(product_id: int, resp: Response, start: int = 0, token: VerifyBody = Depends(auth_method)):

    if not token.success:
        return token.payload

    with scope() as sess:
        reviews = sess.query(Rating).filter(Rating.product_id == product_id).offset(start).limit(10).all()
        if not reviews:
            resp.status_code = 404
            return {"success" : False, "message": "No matching results"}
        
        return [
            {
                "id" : review.id,
                "rating" : review.rating,
                "comment" : review.comment,
                "images" : review.images.split(","),
                "uploaded_at" : review.uploaded_at,
                "updated_at" : review.updated_at
            } for review in reviews
        ]