from pydantic import BaseModel, Field

from App.database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, id, name, amount, owner_id):
        self.id = id
        self.name = name
        self.amount = amount
        self.owner_id = owner_id


class ExpenseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    amount: int = Field(gt=0, lt=20000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "netflix",
                "amount": 30,
            }
        }
    }
