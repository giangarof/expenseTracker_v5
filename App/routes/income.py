from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schema.Income import Income, IncomeRequest
from App.schema.Expense import Expense, ExpenseRequest
from App.database.database import get_db, db_dependency
from App.utilities.auth import get_current_user, user_dependency
from App.utilities.utils import incrementId, checkIfExist

router = APIRouter(prefix="/api/income", tags=["Income"])


# Method: GET
# Route: /api/income/
# Description: Fetch incomes
@router.get("/")
def getIncome(user: user_dependency, db: db_dependency):

    income = db.query(Income).filter(Income.owner_id == user["id"]).all()

    if not income:
        raise HTTPException(status_code=404, detail="Income list is empty...")
    return {"message": "All incomes", "data": income}


# Method: POST
# Route: /api/income/add
# Description: Add income
@router.post("/add")
def add_income(user: user_dependency, db: db_dependency, incomeRequest: IncomeRequest):

    income = Income(
        incrementId(Income, db), incomeRequest.name, incomeRequest.amount, user["id"]
    )

    db.add(income)
    db.commit()
    return {"message": "Income added successfully"}


# Method: PUT
# Route: /api/income/{id}
# Description: Update income
@router.put("/{id}")
def update_income(
    user: user_dependency,
    db: db_dependency,
    incomeRequest: IncomeRequest,
    id: int = Path(gt=0),
):

    income = (
        db.query(Income).filter(Income.owner_id == user["id"], Income.id == id).first()
    )

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income does not exist"
        )

    income.name = incomeRequest.name
    income.amount = incomeRequest.amount

    db.commit()
    return {"message": "Income updated successfully"}


# Method: DELETE
# Route: /api/income/{id}
# Description:Delete income
@router.delete("/{id}")
def delete_income(
    user: user_dependency,
    db: db_dependency,
    id: int = Path(gt=0),
):

    income = (
        db.query(Income).filter(Income.owner_id == user["id"], Income.id == id).first()
    )

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income does not exist"
        )

    db.delete(income)
    db.commit()
    return {"message": "Income deleted successfully"}
