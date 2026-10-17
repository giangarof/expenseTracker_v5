from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.Expense import Expense, ExpenseRequest
from App.database.database import get_db, db_dependency
from App.schema.User import User
from App.utilities.auth import get_current_user, user_dependency
from App.utilities.utils import ifAdmin, incrementId, checkIfExist

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# Method: GET
# Route: /api/admin/user/{id}
# Description: Retrieve one user
@router.get("/user/{id}")
def getOne(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)
    fetchUser = db.query(User).filter(User.id == id).first()
    return fetchUser


# Method: PUT
# Route: /api/admin/update/user/{id}
# Description: Update one user by id
@router.put("/update/user/{id}")
def updateUser(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)
    fetchUser = db.query(User).filter(User.id == id).first()
    return fetchUser
    # complete route


# Method: PUT
# Route: /api/admin/update/expense/{id}
# Description: Update one expense by id
@router.put("/update/expense/{id}")
def updateExpense(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    pass


# Method: DELETE
# Route: /api/admin/delete/expense/{id}
# Description: Delete one expense by id
@router.delete("/delete/expense/{id}")
def deleteExpense(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    pass


# Method: DELETE
# Route: /api/admin/delete/user /{id}
# Description: Delete one user by id
@router.delete("/delete/user/{id}")
def deleteUser(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)
    fetchUser = db.query(User).filter(User.id == id).first()
    return fetchUser
    # complete route
