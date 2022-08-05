from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import BIGINT
from .db import Base

PAGE_SIZE = 20

@dataclass
class QnaData:
    id: int
    product_id: int
    writer_id: int
    content: str
    answer : str | None
    answered_at: str | None
    uploaded_at: str

class Qna(Base):
    __tablename__ = 'qnas'

    id = Column(BIGINT(20), primary_key=True, autoincrement=True)
    product_id = Column(BIGINT(20), nullable=False)
    writer_id = Column(BIGINT(20), nullable=False)
    content = Column(String(1000, 'utf8mb3_bin'), nullable=False)
    answer = Column(String(2000, 'utf8mb3_bin'))
    answered_at = Column(DateTime)
    uploaded_at = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    @staticmethod
    def get_detail(qna: Qna) -> QnaData:
        ans = qna.answered_at

        return QnaData(
            id=qna.id,  # type: ignore
            product_id=qna.product_id,  # type: ignore
            writer_id=qna.writer_id,  # type: ignore
            content=qna.content,  # type: ignore
            answer=qna.answer,  # type: ignore
            answered_at=datetime.isoformat(ans) if ans else None,  # type: ignore
            uploaded_at=datetime.isoformat(qna.uploaded_at)  # type: ignore
        )
    
    @staticmethod
    def session_get_qna(sess, qna_id: int) -> Qna | None:
        return sess.query(Qna).filter(Qna.id == qna_id).first()

    @staticmethod
    def session_get_qnas(sess, product_id: int, offset: int) -> list[Qna]:
        return sess.query(Qna).filter(Qna.product_id == product_id).offset(offset*PAGE_SIZE).limit(PAGE_SIZE).all()

    @staticmethod
    def session_add(sess, product_id: int, writer_id: int, content: str) -> Qna:
        qna = Qna(
            product_id=product_id,
            writer_id=writer_id,
            content=content
        )

        sess.add(qna)
        sess.flush()
        sess.refresh(qna)

        return qna

    @staticmethod
    def session_get_detail(sess, qna_id: int) -> QnaData | None:
        data = sess.query(Qna).filter(Qna.id == qna_id).first()
        return Qna.get_detail(data) if data else data

    @staticmethod
    def session_get_shorts(sess, product_id: int, offset: int = 0) -> list[QnaData]:
        return [Qna.get_detail(qna) for qna in Qna.session_get_qnas(sess, product_id, offset)]
