from typing import Literal
from fastapi import APIRouter, Query
from database import scope, Products

router = APIRouter(prefix="/search")

@router.get("/")
def search(
    query: str = Query(max_length=100, min_length=2),
    mode: Literal['full', 'tag', 'name'] = Query(...)):

    with scope() as sess:
        return Products.session_search_short(sess, query, mode)
