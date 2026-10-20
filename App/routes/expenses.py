from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.Expense import Expense, ExpenseRequest
from App.database.database import get_db, db_dependency
from App.utilities.utils import incrementId, checkIfExist
from App.utilities.auth import get_current_user, user_dependency

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


# Method: GET
# Route: /api/expenses
# Description: Fetch all expenses that
@router.get("/")
def getAll(user: user_dependency, db: db_dependency):

    # Fetch all the data from the user logged in
    data = db.query(Expense).filter(Expense.owner_id == user["id"]).all()

    # If there is no data, raise an error
    if not data:
        raise HTTPException(status_code=404, detail="You have no expenses...")

    # Otherwise, return data
    return {"message": "Fetching all expenses", "data": data}


# Method: GET
# Route: /api/expenses/{id}
# Description: Fetch expense by id
@router.get("/{id}")
def getOne(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):

    # Check if the id exist
    # data = checkIfExist(db, Expense, id)
    data = (
        db.query(Expense)
        .filter(Expense.owner_id == user["id"], Expense.id == id)
        .first()
    )

    # If the id doesnt exist, raise an error
    if not data:
        raise HTTPException(status_code=404, detail="Expense does not exist")

    # Otherwise, return the data
    return {"message": "Expense found", "data": data}


# Method: POST
# Route: /api/expenses
# Description: Add a new expense
@router.post("/", status_code=status.HTTP_201_CREATED)
async def addNew(user: user_dependency, db: db_dependency, theExpense: ExpenseRequest):

    # Here, increment id is a helper function that takes the expenses and assign a incremented id
    data = Expense(
        incrementId(Expense, db), theExpense.name, theExpense.amount, user["id"]
    )

    # Proceed to save the data
    db.add(data)
    db.commit()
    return {"message": "added successfully", "data": theExpense}


# Method: PUT
# Route: /api/expenses/{id}
# Description: Update expense by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
def updateById(
    user: user_dependency,
    db: db_dependency,
    theExpense: ExpenseRequest,
    id: int = Path(gt=0),
):
    # Check if id exist
    # data = checkIfExist(db, Expense, id)
    data = (
        db.query(Expense)
        .filter(Expense.owner_id == user["id"], Expense.id == id)
        .first()
    )

    # If there is no data
    if not data:
        raise HTTPException(status_code=404, detail="Expense does not exist")

    # Otherwise, proceed to update
    data.name = theExpense.name
    data.amount = theExpense.amount
    db.commit()
    return {"message": "Expense updated", "data": theExpense}


# Method: DELETE
# Route: /api/expenses/{id}
# Description: Delete expense by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def deleteById(user: user_dependency, db: db_dependency, id: int):

    # Check if expense exist
    data = (
        db.query(Expense)
        .filter(Expense.owner_id == user["id"], Expense.id == id)
        .first()
    )

    # Raise an error if there is no data
    if not data:
        raise HTTPException(status_code=404, detail="Expense does not exist")

    # If there is data, the proceed to delete
    db.delete(data)
    db.commit()
    return {"message": "Expense deleted"}
