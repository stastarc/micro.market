from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import BIGINT
from .db import Base

PAGE_SIZE = 20

@dataclass
class ShortQnaData:
    id: int
    writer_id: int
    content: str
    answered: bool

@dataclass
class FullQnaData:
    id: int
    product_id: int
    writer_id: int
    content: str
    answer : str | None
    answered_at: str | None
    uploaded_at: str

class Qna(Base):
    __tablename__ = 'qnas'

    id = Column(BIGINT(20), primary_key=True)
    product_id = Column(BIGINT(20), nullable=False)
    writer_id = Column(BIGINT(20), nullable=False)
    content = Column(String(5000, 'utf8mb3_bin'), nullable=False)
    answer = Column(String(5000, 'utf8mb3_bin'))
    answered_at = Column(DateTime)
    uploaded_at = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    @staticmethod
    def session_get_qnas(sess, product_id: int, offset: int) -> list[Qna]:
        return sess.query(Qna).filter(Qna.product_id == product_id).offset(offset).limit(PAGE_SIZE).all()

    @staticmethod
    def parse_qna_object_to_dict_full(qna: Qna) -> FullQnaData:
        return FullQnaData(
            id=qna.id,
            product_id=qna.product_id,
            writer_id=qna.writer_id,
            content=qna.content,
            answer=qna.answer,
            answered_at=qna.answered_at,
            uploaded_at=qna.uploaded_at
        )

    @staticmethod
    def parse_qna_object_to_dict_short(qna: Qna) -> ShortQnaData:
        return ShortQnaData(
            id=qna.id,
            writer_id=qna.writer_id,
            content=qna.content,
            answered=qna.answer is not None
        )

    @staticmethod
    def session_get_qna(sess, qna_id: int) -> Qna:
        return sess.query(Qna).filter(Qna.id == qna_id).first()

    @staticmethod
    def session_write_qna(sess, product_id: int, writer_id: int, content: str) -> Qna:
        qna = Qna(product_id=product_id, writer_id=writer_id, content=content)
        sess.add(qna)
        return qna

    @staticmethod
    def session_get_specific_qna_short(sess, qna_id: int) -> ShortQnaData | None:
        qna = sess.query(Qna).filter(Qna.id == qna_id).first()
        if not qna:
            return None
        return ShortQnaData(id=qna.id, writer_id=qna.writer_id, content=qna.content, answered=bool(qna.answer))

    @staticmethod
    def session_get_specific_qna_full(sess, qna_id: int) -> FullQnaData | None:
        qna = sess.query(Qna).filter(Qna.id == qna_id).first()
        if not qna:
            return None
        return FullQnaData(id=qna.id, product_id=qna.product_id, writer_id=qna.writer_id, content=qna.content, answer=qna.answer, answered_at=str(qna.answered_at) if qna.answered_at else None, uploaded_at=str(qna.uploaded_at))