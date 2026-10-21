from pydantic import BaseModel, Field

from App.database.database import Base
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# BASE MODEL
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(10), default="basic", nullable=False)

    def __init__(self, id, name, username, email, password, role="basic"):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.role = role


# SIGNUP REQUEST
class UserRequest(BaseModel):

    name: str = Field(min_length=2, max_length=40)
    username: str = Field(min_length=2, max_length=40)
    email: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8, max_length=40)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "jhon doe",
                "username": "jdoe",
                "email": "jhon@gmail.com",
                "password": "password",
            }
        }
    }
