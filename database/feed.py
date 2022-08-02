from sqlalchemy import INTEGER, Column
from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from .db import Base

class Feed(Base):
    __tablename__ = 'feeds'

    index = Column(INTEGER, nullable=False, index=True, primary_key=True)
    title = Column(VARCHAR(100), nullable=False)
    content_type = Column(ENUM('tag', 'name'), nullable=False)
    content = Column(VARCHAR(1000), nullable=False)