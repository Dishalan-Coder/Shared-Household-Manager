from models.chore import Chore
from sqlalchemy.orm import Session


class ChoreService:

    @staticmethod
    def create_chore(db: Session, data, household_id: int):
        chore = Chore(
            title=data.title,
            assigned_to=data.assigned_to,
            due_date=data.due_date,
            household_id=household_id
        )
        db.add(chore)
        db.commit()
        db.refresh(chore)
        return chore

    @staticmethod
    def complete_chore(db: Session, chore_id: int):
        chore = db.query(Chore).filter(Chore.id == chore_id).first()
        if chore:
            chore.is_done = True
            db.commit()
        return chore