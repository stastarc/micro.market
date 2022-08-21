from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, BIT
from .db import Base

@dataclass
class RecommendedItem:
    goto: int
    image: str
    name: str
    content: str

@dataclass
class RecommendedData:
    id: int
    items: Iterable[RecommendedItem]
    title: str
    content: str
    is_end: bool

class Recommended(Base):
    __tablename__ = 'recommended'

    id = Column(BIGINT, nullable=False, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    title = Column(VARCHAR(50), nullable=False)
    items = Column(VARCHAR(500), nullable=False)
    content = Column(VARCHAR(500), nullable=False)
    is_end = Column(BIT, nullable=False)

    @staticmethod
    def parse_items(items: str) -> Iterable[RecommendedItem]:
        for item in items.split('\n'):
            if not item:
                continue

            cs = item.split(':')

            if len(cs) != 4:
                continue

            name, content, image, goto = cs
            yield RecommendedItem(
                goto=int(goto),
                image=image,
                name=name,
                content=content
            )
    

    @staticmethod
    def session_get(sess, id: int) -> Recommended | None:
        return sess.query(Recommended).filter(Recommended.id == id).first()

    @staticmethod
    def session_data(data: Recommended) -> RecommendedData:
        return RecommendedData(
            id=data.id,  # type: ignore
            title=data.title,  # type: ignore
            content=data.content,  # type: ignore
            items=list(Recommended.parse_items(data.items)),  # type: ignore
            is_end=data.is_end == 1 # type: ignore
        )

    @staticmethod
    def session_get_data(sess, id: int) -> RecommendedData | None:
        data = sess.query(Recommended).filter(Recommended.id == id).first()
        
        if not data:
            return None

        return Recommended.session_data(data)
