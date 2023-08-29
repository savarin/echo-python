# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EchoLog(Base):  # type: ignore
    __tablename__ = "echo_log"

    id = Column(String, primary_key=True)
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
