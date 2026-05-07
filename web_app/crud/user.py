from web_app.models import User, ModelError
from sqlmodel import Session, select
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def get_user_by_user_name(user_name: str, session: Session) -> User | ModelError:
    """
    Returns a User for the provided user_name.

    In case of success, a User table model is returned. In case of error a ModelError enum is returned:
    - USER_NAME_NOT_FOUND, if user_name not found in db
    - DATABASE_ERROR, in case of other errors
    """
    try:
        user = session.exec(select(User).where(User.user_name == user_name)).first()
        if not user:
            return ModelError.USER_NAME_NOT_FOUND
        return user
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ModelError.DATABASE_ERROR


def get_user_by_id(id: int, session: Session) -> User | ModelError:
    """
    Returns a User for the provided user id.

    In case of success, a User table model is returned. In case of error a ModelError enum is returned:
    - USER_ID_NOT_FOUND, if user_name not found in db
    - DATABASE_ERROR, in case of other errors
    """
    try:
        user = session.get(User, id)
        if not user:
            return ModelError.USER_ID_NOT_FOUND
        return user
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ModelError.DATABASE_ERROR


def add_user_to_db(user: User, session: Session) -> User | ModelError:
    """
    Adds a User to the db session and commits it.

    In case of success, the User table model is returned. In case of error a ModelError enum is returned:
    - VALIDATION_ERROR, if provided user cannot be validated to a User table model
    - USER_NAME_ALREADY_EXISTS, if user_name of the provided user already exists
    - DATABASE_ERROR, in case of other errors
    """
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user  # Success: Return the object directly
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
