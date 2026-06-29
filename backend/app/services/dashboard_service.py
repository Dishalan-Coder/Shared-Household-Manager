from models.chore import Chore
from models.expense import Expense
from models.grocery import GroceryItem
from sqlalchemy.orm import Session


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session, household_id: int):

        chores = db.query(Chore).filter(Chore.household_id == household_id).count()
        expenses = db.query(Expense).filter(Expense.household_id == household_id).all()
        groceries = db.query(GroceryItem).filter(GroceryItem.household_id == household_id).count()

        total_expense = sum(e.amount for e in expenses)

        return {
            "total_chores": chores,
            "total_grocery_items": groceries,
            "total_expense": total_expense
        }