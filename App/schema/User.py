from pydantic import BaseModel, Field

from App.database.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)

    def __init__(self, id, first_name, last_name, email, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class UserRequest(BaseModel):
    # id = Column(Integer, primary_key=True, index=True)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=1, max_length=50)
    phone: str = Field(max_length=35)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "jhon",
                "last_name": "doe",
                "email": "test@test.com",
                "phone": "+1 2223334455",
            }
        }
    }
