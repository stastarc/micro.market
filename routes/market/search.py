from typing import Literal
from fastapi import APIRouter, Depends, Query
from database import scope, Products
import database.products as products

from micro import VerifyBody, auth_method

router = APIRouter(prefix="/search")

@router.get("/")
def search(
    query: str = Query(max_length=100, min_length=2),
    mode: Literal['full', 'tag', 'name'] = Query(...),
    token: VerifyBody = Depends(auth_method)):
    
    if not token.success:
        return token.payload

    with scope() as sess:
        return {
            'query': query,
            'products': Products.session_search_short(sess, query, mode),
            'page': max(Products.session_search_count(sess, query, mode) // products.PAGE_SIZE, 1),
            'size': products.PAGE_SIZE
        }
