from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.Token import Token
from App.schema.User import User, UserRequest
from App.database.database import get_db, db_dependency
from App.utilities.auth import authenticate_user, create_access_token, user_dependency
from App.utilities.utils import hashPassword, incrementId, verify_password

router = APIRouter(prefix="/api/user", tags=["Users"])


# Method: POST
# Route: /api/user/login
# Description: Login an existing user
@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = db.query(User).filter(User.username == form_data.username).first()
    # check if user exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    verify_password(form_data.password, user.password)
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# Method: POST
# Route: /api/user/signup
# Description: Add a new user to the db
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, userRequest: UserRequest):
    # Fetch all users
    # users = db.query(User).all()

    # Generate ID
    new_id = await incrementId(User, db)
    # Hash password
    hashed = await hashPassword(userRequest.password)

    # Create and add new user
    new_user = User(
        new_id,
        userRequest.name,
        userRequest.username,
        userRequest.email,
        hashed,
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully", "data": userRequest}


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
# Route: /api/user/profile
# Description: Retrive the logged user information
@router.get("/profile")
def profile(user: user_dependency, db: db_dependency):
    theUser = db.query(User).filter(User.id == user["id"]).first()
    return theUser


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


@router.post("/token", response_model=Token)
async def login_for_acces_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db, User)

    if not user:
        raise HTTPException(status_code=400, detail="Failed authentication")

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
