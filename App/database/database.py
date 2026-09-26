from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database connection URL that tells SQLAlchemy which database to connect to and where it is located.
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Create the engine
# Engine is the object that SQLAlchemy uses to communicate with your database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# sessionmaker() is a SQLAlchemy function that creates a session factory.
# SessionLocal creates sessions that actually perform database work.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class that your database model classes inherit from.
# declarative_base() creates a special base class for SQLAlchemy ORM models.
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
