from sqlalchemy.orm import Session
from models.user import User
from utils.security import hash_password, verify_password, create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, user_data):
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.password):
            return None

        token = create_access_token({"user_id": user.id})
        return {"access_token": token, "user": user}