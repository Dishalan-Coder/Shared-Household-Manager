from models.household import Household
from sqlalchemy.orm import Session


class HouseholdService:

    @staticmethod
    def create_household(db: Session, name: str, owner_id: int):
        household = Household(name=name, owner_id=owner_id)
        db.add(household)
        db.commit()
        db.refresh(household)
        return household

    @staticmethod
    def join_household(db: Session, household_id: int, user_id: int):
        household = db.query(Household).filter(Household.id == household_id).first()
        if not household:
            return None

        household.members.append(user_id)
        db.commit()
        return household