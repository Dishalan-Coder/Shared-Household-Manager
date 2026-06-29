from models.expense import Expense
from sqlalchemy.orm import Session


class ExpenseService:

    @staticmethod
    def add_expense(db: Session, data, household_id: int):
        expense = Expense(
            title=data.title,
            amount=data.amount,
            paid_by=data.paid_by,
            household_id=household_id
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_expenses(db: Session, household_id: int):
        return db.query(Expense).filter(Expense.household_id == household_id).all()