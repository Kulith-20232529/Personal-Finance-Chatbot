from fastapi import APIRouter
from services.expense_service import (
    get_all_expenses,
    delete_expense_by_id,
    update_expense_by_id
)

router = APIRouter()


@router.get("/transactions")
def get_transactions():
    return get_all_expenses()


@router.delete("/transactions/{expense_id}")
def delete_transaction(expense_id: str):
    delete_expense_by_id(expense_id)
    return {"message": "Deleted"}


@router.put("/transactions/{expense_id}")
def update_transaction(expense_id: str, data: dict):
    update_expense_by_id(expense_id, data)
    return {"message": "Updated"}