from typing import Literal
from fastapi import APIRouter, Depends, Response
from database import scope, Rating, Product
from micro import auth_method, VerifyBody


router = APIRouter()

@router.get("/{product_id}/reviews")
def product_desc(product_id: int, offset: int = 0, orderby: Literal['last', 'high', 'low'] = 'high', token: VerifyBody = Depends(auth_method)):

    if not token.success:
        return token.payload

    with scope() as sess:
        if not Product.session_exists(sess, product_id):
            return Response(status_code=404)

        return {
            'average': Rating.session_get_average_rating(sess, product_id),
            'ratings': Rating.session_get_ratings(sess, product_id, offset, orderby),
        }
