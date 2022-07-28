# 없애면 안돼ㅑ요~
from .db import engine, factory, scope
import random
import string

from sqlalchemy import Column, DateTime, text, exists
from sqlalchemy.dialects.mysql import BIGINT, ENUM, VARCHAR
from .db import Base
from utils import nickname as nickname_util

class Product(Base):
    __tablename__ = 'products'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    price = Column(BIGINT, nullable=False)
    delivery_fee = Column(BIGINT, nullable=False)
    tags = Column(VARCHAR(1000), nullable=False)
    title = Column(VARCHAR(100), nullable=False)
    name = Column(VARCHAR(200), nullable=False)
    info = Column(VARCHAR(1000), nullable=False)
    images = Column(VARCHAR(320), nullable=False)
    con

    @staticmethod
    def exists_nickname(sess, nickname) -> bool:
        return sess.query(exists().where(User.nickname == nickname)).scalar()

    @staticmethod
    def create_nickname(sess) -> str: # idk session type :(
        while True:
            nickname = f'{nickname_util.choice()}_{"".join(random.choices(string.digits, k=8))}'

            if not User.exists_nickname(sess, nickname):
                return nickname
