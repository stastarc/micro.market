from .db import engine, factory, scope
from sqlalchemy import Column, DateTime, Index, String, Text, text, exists
from sqlalchemy.dialects.mysql import BIGINT, ENUM, VARCHAR, TINYINT
from .db import Base
from sqlalchemy.sql.functions import func

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    product_id = Column(BIGINT(20), nullable=False)
    rating = Column(TINYINT(3), nullable=False, comment='1~5')
    comment = Column(String(2000, 'utf8mb3_bin'), nullable=False)
    images = Column(Text(collation='utf8mb3_bin'), nullable=False)
    updated_at = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    uploaded_at = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    @staticmethod
    def session_get_average_rating(session, product_id: int) -> float:
        return float(session.query(func.avg(Rating.rating)).filter(Rating.product_id == product_id).scalar() or 0.0)
