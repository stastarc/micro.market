
from dataclasses import dataclass
from typing import Literal
from .product import Product
from .rating import Rating


PAGE_SIZE = 20

@dataclass
class ProductOption:
    name: str
    price: int
    important: bool

    @staticmethod
    def parse_options(option: str) -> list['ProductOption']:
        if not option: return []
        options = option.split('\n')
        ops = []

        for op in options:
            if not op: continue
            name, price = op.split(':')
            imp = op[0] == '!'
            ops.append(ProductOption(name[1 if imp else 0:], int(price), imp))
        
        return ops

@dataclass
class ShortProductData:
    id: int
    title: str
    price: int
    image: str
    rating: float

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
    component: str
    options: list[ProductOption]
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
    def get_short(sess, product: Product) -> ShortProductData:
        images = Product.parse_images(product.images)  # type: ignore
        return ShortProductData(
            id=product.id,   # type: ignore
            title=product.title,   # type: ignore
            price=product.price,   # type: ignore
            image=images[0] if images else '',
            rating=Rating.session_get_average_rating(sess, product.id)  # type: ignore
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
            component=product.component,   # type: ignore
            options=ProductOption.parse_options(product.options),   # type: ignore
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
        return [Products.get_short(sess, product) for product in products]

    @staticmethod
    def session_get_detail(sess, product_id: int) -> DetailProductData | None:
        product = sess.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return None
        return Products.get_detail(sess, product)