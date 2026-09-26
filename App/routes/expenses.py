from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.Expense import Expense, ExpenseRequest
from App.database.database import get_db, db_dependency
from utilities.utilities import incrementId, checkIfExist

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


# Method: GET
# Route: /api/expenses
# Description: Fetch all expenses
@router.get("/")
def getAll(db: db_dependency):

    # Fetch all the data
    data = db.query(Expense).all()

    # If there is no data, raise an error
    if not data:
        raise HTTPException(status_code=404, detail="Nothing on the DB...")

    # Otherwise, return data
    return {"message": "Fetching all expenses", "data": data}


# Method: GET
# Route: /api/expenses/{id}
# Description: Fetch expense by id
@router.get("/{id}")
def getOne(db: db_dependency, id: int = Path(gt=0)):

    # Check if the id exist
    data = checkIfExist(db, Expense, id)

    # If the id doesnt exist, raise an error
    if not data:
        raise HTTPException(status_code=404, detail="Id doesnt exist")

    # Otherwise, return the data
    return {"message": "Expense found", "data": data}


# Method: POST
# Route: /api/expenses
# Description: Add a new expense
@router.post("/", status_code=status.HTTP_201_CREATED)
async def addNew(db: db_dependency, theExpense: ExpenseRequest):

    # Get all the expenses first to assign a incremented id
    expenses = db.query(Expense).all()

    # Here, increment id is a helper function that takes the expenses and assign a incremented id
    data = Expense(incrementId(expenses), theExpense.name, theExpense.amount)

    # Proceed to save the data
    db.add(data)
    db.commit()
    return {"message": "added successfully", "data": theExpense}


# Method: PUT
# Route: /api/expenses/{id}
# Description: Update expense by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
def updateById(db: db_dependency, theExpense: ExpenseRequest, id: int = Path(gt=0)):
    # Check if id exist
    data = checkIfExist(db, Expense, id)

    # If there is no data
    if not data:
        raise HTTPException(status_code=404, detail="Id doesnt exist")

    # Otherwise, proceed to update
    data.name = theExpense.name
    data.amount = theExpense.amount
    db.commit()
    return {"message": "Expense updated", "data": theExpense}


# Method: DELETE
# Route: /api/expenses/{id}
# Description: Delete expense by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def deleteById(db: db_dependency, id: int):

    # Check if id exist
    data = checkIfExist(db, Expense, id)

    # Raise an error if there is no data
    if not data:
        raise HTTPException(status_code=404, detail="Id doesnt exist")

    # If there is data, the proceed to delete
    db.delete(data)
    db.commit()
    return {"message": "Expense deleted"}
