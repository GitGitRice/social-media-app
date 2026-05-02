from web_app.models import User, UserCreate, UserCreateError
from sqlmodel import Session, select
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from typing import Sequence

def add_user_to_db(user: UserCreate, session: Session) -> User | UserCreateError:
    try:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user  # Success: Return the object directly
    except ValidationError as e:
        print(f"ValidationError: {e}")
        return UserCreateError.VALIDATION_ERROR
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        session.rollback()
        return UserCreateError.ALREADY_EXISTS
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        return UserCreateError.DATABASE_ERROR
    
def get_users_from_db(session: Session) -> list[User]:
    statement = select(User)
    users = session.exec(statement).all()

    # cast to return value of function. SQLModel .all() is returning Sequence[User]
    return list(users) 