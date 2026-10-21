from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String

from App.database.database import Base


class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    amount = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, id, name, amount, owner_id):
        self.id = id
        self.name = name
        self.amount = amount
        self.owner_id = owner_id


class IncomeRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    amount: int = Field(gt=0, lt=100000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "main income",
                "amount": 50000,
            }
        }
    }
