from web_app.models import User, UserCreate, ModelError
from sqlmodel import Session, select
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from typing import Sequence

def add_user_to_db(user: UserCreate, session: Session) -> User | ModelError:
    """
    Adds a UserCreate to the db session and commits it.
    
    In case of success, the User table model is returned. In case of error a ModelError enum is returned.
    """
    try:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user  # Success: Return the object directly
    except ValidationError as e:
        print(f"ValidationError: {e}")
        return ModelError.VALIDATION_ERROR
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        session.rollback()
        return ModelError.USER_NAME_ALREADY_EXISTS
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR
    
def get_users_from_db(session: Session) -> list[User]:
    """
    Returns a list of User table models from the db session.
    """
    statement = select(User)
    users = session.exec(statement).all()

    # cast to return value of function. SQLModel .all() is returning Sequence[User]
    return list(users) 