from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.database.database import get_db, db_dependency

from App.schema.Expense import Expense, ExpenseRequest
from App.schema.User import User, UserRequest
from App.schema.Income import Income, IncomeRequest

from App.utilities.auth import get_current_user, user_dependency
from App.utilities.utils import hashPassword, ifAdmin, incrementId, checkIfExist

router = APIRouter(prefix="/api/admin", tags=["Admin"])


## USER


# Method: GET
# Route: /api/admin/user/{id}
# Description: Retrieve one user
@router.get("/user/{id}")
def getOne(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)
    fetchUser = db.query(User).filter(User.id == id).first()
    if not fetchUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return fetchUser


# Method: PUT
# Route: /api/admin/update/user/{id}
# Description: Update one user by id
@router.put("/update/user/{id}")
async def updateUser(
    user: user_dependency,
    db: db_dependency,
    userRequest: UserRequest,
    id: int = Path(gt=0),
):
    ifAdmin(user)

    # Hash password
    fetchUser = db.query(User).filter(User.id == id).first()
    hashed = await hashPassword(userRequest.password)

    if not fetchUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    # Replace fields
    fetchUser.name = userRequest.name
    fetchUser.username = userRequest.username
    fetchUser.email = userRequest.email
    fetchUser.password = hashed
    # Save to the db
    db.commit()
    return {"message": "User updated successfully"}
    # complete route


# Method: DELETE
# Route: /api/admin/delete/user /{id}
# Description: Delete one user by id
@router.delete("/delete/user/{id}")
def deleteUser(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)

    fetchUser = db.query(User).filter(User.id == id).first()

    if not fetchUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if user["role"] == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot be deleted by himself",
        )

    db.delete(fetchUser)
    db.commit()

    return {"message": "User deleted successfully"}


## EXPENSES


# Method: PUT
# Route: /api/admin/update/expense/{id}
# Description: Update one expense by id
@router.put("/update/expense/{id}")
def updateExpense(
    user: user_dependency,
    db: db_dependency,
    expenseRequest: ExpenseRequest,
    id: int = Path(gt=0),
):
    ifAdmin(user)

    expense = db.query(Expense).filter(Expense.id == id).first()
    expense.name = expenseRequest.name
    expense.amount = expenseRequest.amount

    db.commit()

    return {"message": "Expense updated successfully"}


# Method: DELETE
# Route: /api/admin/delete/expense/{id}
# Description: Delete one expense by id
@router.delete("/delete/expense/{id}")
def deleteExpense(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)

    expense = db.query(Expense).filter(Expense.id == id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense does not exist"
        )

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


## INCOME


# Method: GET
# Route: /api/admin/incomes/
# Description: Retrieve all incomes from all users
@router.get("/incomes/")
def getAllIncomes(user: user_dependency, db: db_dependency):
    ifAdmin(user)
    fetchIncomes = db.query(Income).all()

    if not fetchIncomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income list is empty."
        )

    return {"message": "All incomes fetched", "data": fetchIncomes}


# Method: PUT
# Route: /api/admin/update/income/{id}
# Description: Update income by id
@router.put("/update/income/{id}")
def updateIncome(
    user: user_dependency,
    db: db_dependency,
    incomeRequest: IncomeRequest,
    id: int = Path(gt=0),
):
    ifAdmin(user)
    income = db.query(Income).filter(Income.id == id).first()

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income does not exist"
        )

    income.name = incomeRequest.name
    income.amount = incomeRequest.amount

    db.commit()

    return {"message": "Income updated successfully"}


# Method: DELETE
# Route: /api/admin/delete/income/{id}
# Description: Delete income by id
@router.delete("/delete/income/{id}")
def deleteIncome(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    ifAdmin(user)
    income = db.query(Income).filter(Income.id == id).first()

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income does not exist"
        )
    db.delete(income)
    db.commit()

    return {"message": "Income deleted successfully"}
