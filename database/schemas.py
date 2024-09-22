from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RM6Base(BaseModel):
    serial: str
    cause: str
    storage: str
    date_in: datetime

class RM6Create(RM6Base):
    pass;

class RM6(RM6Base):
    id: int
    date_out: datetime