from models.expense import Expense
from models.user import User
from sqlalchemy.orm import Session


class BalanceService:

    @staticmethod
    def calculate_balances(db: Session, household_id: int):
        expenses = db.query(Expense).filter(Expense.household_id == household_id).all()

        balance_map = {}

        for exp in expenses:
            payer = exp.paid_by
            amount = exp.amount

            if payer not in balance_map:
                balance_map[payer] = 0

            balance_map[payer] += amount

        return balance_map