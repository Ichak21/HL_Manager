from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base

class Rm6(Base):
    __tablename__ = 'RM6'
    id = Column(Integer, primary_key=True, autoincrement=True)
    serial = Column(String, nullable=False)
    cause = Column(String, nullable=False)
    storage = Column(String, nullable=False)
    date_in = Column(DateTime, nullable=False)
    date_out = Column(DateTime, nullable=True)

    def display_row_table(self):
        if self.date_out == None:
            return (self.serial, self.cause, self.storage, self.date_in.strftime("%d/%m/%Y %H:%M:%S"), self.date_out)
        else:
            return (self.serial, self.cause, self.storage, self.date_in.strftime("%d/%m/%Y %H:%M:%S"), self.date_out.strftime("%d/%m/%Y %H:%M:%S"))