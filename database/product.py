from __future__ import annotations
from sqlalchemy import Column, DateTime, String, text, exists
from sqlalchemy.dialects.mysql import BIGINT, MEDIUMTEXT
from .db import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(BIGINT(20), primary_key=True, nullable=False)
    tags = Column(String(500, 'utf8mb3_bin'), nullable=False, index=True, comment='키우기 쉬운,공기정화')
    price = Column(BIGINT(20), nullable=False)
    delivery_fee = Column(BIGINT(20), nullable=False)
    title = Column(String(100, 'utf8mb3_bin'), nullable=False)
    name = Column(String(200, 'utf8mb3_bin'), nullable=False)
    info = Column(String(1000, 'utf8mb3_bin'), nullable=False)
    images = Column(String(320, 'utf8mb3_bin'), nullable=False, comment='이미지 최대 10장')
    component = Column(String(1000, 'utf8mb3_bin'), nullable=False)
    options = Column(String(1000, 'utf8mb3_bin'), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    updated_at = Column(DateTime)
    uploaded_at = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    @staticmethod
    def parse_images(images: str) -> list[str]:
        count = len(images) // 32
        return [images[i*32:(i+1)*32] for i in range(count)] or []

    @staticmethod
    def session_exists(sess, product_id: int) -> bool:
        return sess.query(exists().where(Product.id == product_id)).scalar()
