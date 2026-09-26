from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.User import User, UserRequest
from App.database.database import get_db, db_dependency

router = APIRouter(prefix="/api/user", tags=["Users"])


# Method: POST
# Route: /api/user/login
# Description: Login an existing user
@router.post("/")
def login():
    return "login"


# Method: POST
# Route: /api/user/signup
# Description: Add a new user to the db
@router.post("/")
def signup():
    return "signup"


# Method: POST
# Route: /api/user/logout
# Description: Logout a user that is login
@router.post("/")
def logout():
    return "logout"


# Method: GET
# Route: /api/user/users
# Description: Fetch all the users
@router.get("/users", status_code=status.HTTP_200_OK)
def fetchAll(db: db_dependency):
    data = db.query(User).all()
    if not data:
        raise HTTPException(status_code=400, detail="nothing found")
    return {"message": "All users", "data": data}


# Method: GET
# Route: /api/user/{id}
# Description: Fetch the first user that matches by id
@router.get("/")
def getUser():
    return "logout"


# Method: PUT
# Route: /api/user/update/{id}
# Description: Update an existing user by id
@router.put("/")
def updateUser():
    return "logout"


# Method: DELETE
# Route: /api/user/{id}
# Description: Delete an existing user by id
@router.delete("/")
def deleteUser():
    return "logout"
