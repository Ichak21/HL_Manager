from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base

class Rm6(Base):
    __tablename__ = 'RM6'
    serial = Column(String, primary_key=True)
    cause = Column(String, nullable=False)
    storage = Column(String, nullable=False)
    date_in = Column(DateTime, nullable=False)
    date_out = Column(DateTime, nullable=True)