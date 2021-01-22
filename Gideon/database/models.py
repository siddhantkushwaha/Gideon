from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index

Base = declarative_base()


class Newspaper(Base):
    __tablename__ = 'newspaper'
    __table_args__ = (
        Index('unique_constraint', 'name', 'edition', 'language', 'type', 'timestamp', unique=True),
    )

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    edition = Column(String, nullable=False)
    language = Column(String, nullable=False)
    type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    link = Column(String, nullable=False)
    drive_file_id = Column(String, nullable=False)


models = [
    Newspaper
]
