
from dataclasses import dataclass
from typing import Literal
from .product import Product
from .rating import Rating

from sqlalchemy.sql.expression import func

PAGE_SIZE = 20

@dataclass
class ShortProductData:
    id: int
    name: str
    price: int
    image: str

@dataclass
class DetailProductData:    
    id: int
    price: int
    delivery_fee: int
    title: str
    name: str
    info: str
    rating: float
    images: list[str]
    content: str

class Products:
    @staticmethod
    def fulltext_search_against(mode: Literal['full', 'tag', 'name']) -> str:
        return f'MATCH ({"tags, title, name, info" if mode == "full" else "tags" if mode == "tag" else "name"}) AGAINST (:q IN BOOLEAN MODE)'

    @staticmethod
    def session_search(sess, query: str, mode: Literal['full', 'tag', 'name'], offset: int = 0, limit: int = PAGE_SIZE) -> list[Product]:
        fulltext = Products.fulltext_search_against(mode)
        return sess.execute(
            f'SELECT *, {fulltext} as score FROM `{Product.__tablename__}` WHERE {fulltext} ORDER BY score DESC LIMIT {offset*PAGE_SIZE},{limit}',
            {'q': query}).all()
        
    @staticmethod
    def session_search_one(sess, query: str, mode: Literal['full', 'tag', 'name']) -> Product | None:
        fulltext = Products.fulltext_search_against(mode)
        return sess.execute(f'SELECT *, {fulltext} as score FROM `{Product.__tablename__}` WHERE {fulltext} LIMIT 1',
            {'q': query}).first()

    @staticmethod
    def get_short(product: Product) -> ShortProductData:
        return ShortProductData(
            id=product.id,   # type: ignore
            name=product.name,   # type: ignore
            price=product.price,   # type: ignore
            image=Product.parse_images(product.images)[0]  # type: ignore
        )

    @staticmethod
    def get_detail(sess, product: Product) -> DetailProductData:
        return DetailProductData(
            id=product.id,   # type: ignore
            price=product.price,   # type: ignore
            delivery_fee=product.delivery_fee,   # type: ignore
            title=product.title,   # type: ignore
            name=product.name,   # type: ignore
            info=product.info,   # type: ignore
            rating=Rating.session_get_average_rating(sess, product.id),  # type: ignore
            images=Product.parse_images(product.images),  # type: ignore
            content=product.content  # type: ignore
        )
    
    @staticmethod
    def session_search_detail(sess, query: str, mode: Literal['full', 'tag', 'name']) -> DetailProductData | None:
        product = Products.session_search_one(sess, query, mode)
        if product is None:
            return None
        return Products.get_detail(sess, product)

    @staticmethod
    def session_search_short(sess, query: str, mode: Literal['full', 'tag', 'name']) -> list[ShortProductData]:
        products = Products.session_search(sess, query, mode)
        return [Products.get_short(product) for product in products]

    @staticmethod
    def session_get_detail(sess, product_id: int) -> DetailProductData | None:
        product = sess.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return None
        return Products.get_detail(sess, product)