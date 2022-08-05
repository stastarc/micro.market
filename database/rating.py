from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.sql.functions import func
from .db import Base

PAGE_SIZE = 10

@dataclass
class RatingData:
    id: int
    rating: int
    comment: str
    images: str
    updated_at: str


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    product_id = Column(BIGINT(20), nullable=False)
    rating = Column(TINYINT(3), nullable=False, comment='1~5')
    comment = Column(String(2000, 'utf8mb3_bin'), nullable=False)
    images = Column(Text(collation='utf8mb3_bin'), nullable=False)
    updated_at = Column(DateTime, nullable=False, server_default=text("current_timestamp() on update current_timestamp()"))

    @staticmethod
    def parse_images(images: str) -> list[str]:
        count = len(images) // 32
        return [images[i*32:(i+1)*32] for i in range(count)] or ['']

    @staticmethod
    def session_get_average_rating(session, product_id: int) -> float:
        return float(session.query(func.avg(Rating.rating)).filter(Rating.product_id == product_id).scalar() or 0.0)

    @staticmethod
    def session_ratings(sess, product_id: int, offset: int = 0, orderby: Literal['last', 'high', 'low'] = 'high') -> list['Rating']:
        return sess.query(Rating).filter(Rating.product_id == product_id) \
            .order_by(Rating.rating.desc() if orderby == 'high' else Rating.rating.asc() if orderby == 'low' else Rating.updated_at.desc()) \
            .offset(offset*PAGE_SIZE).limit(PAGE_SIZE).all()

    @staticmethod
    def get_rating(rating: 'Rating') -> RatingData:
        return RatingData(
            id=rating.id,  # type: ignore
            rating=rating.rating,  # type: ignore
            comment=rating.comment,  # type: ignore
            images=Rating.parse_images(rating.images),  # type: ignore
            updated_at=datetime.isoformat(rating.updated_at),  # type: ignore
        )
    
    @staticmethod
    def session_get_ratings(sess, product_id: int, offset: int, orderby: Literal['last', 'high', 'low'] = 'high') -> list[RatingData]:
        return [Rating.get_rating(rating) for rating in Rating.session_ratings(sess, product_id, offset, orderby)]