from models.grocery import GroceryItem
from sqlalchemy.orm import Session


class GroceryService:

    @staticmethod
    def add_item(db: Session, data, household_id: int):
        item = GroceryItem(
            name=data.name,
            added_by=data.added_by,
            household_id=household_id
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def toggle_item(db: Session, item_id: int):
        item = db.query(GroceryItem).filter(GroceryItem.id == item_id).first()
        if item:
            item.is_checked = not item.is_checked
            db.commit()
        return item