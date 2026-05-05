from web_app.models import User, UserCreate, Post, PostCreate, ModelError
from sqlmodel import Session, select
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

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

def create_post(post_data: PostCreate, session: Session) -> Post | ModelError:
    """Inserts a new post into the database."""
    try:
        db_post = Post.model_validate(post_data)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post
    except Exception as e:
        print(f"Error creating post: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR
    
def get_posts(session: Session, offset: int = 0, limit: int = 10) -> List[Post]:
    """Fetches a paginated list of all public posts (Global Feed)."""
    statement = select(Post).offset(offset).limit(limit).order_by(Post.created_at.desc())
    return list(session.exec(statement).all())

def get_post_by_id(session: Session, post_id: int) -> Optional[Post]:
    """Fetches a single post by its ID."""
    return session.get(Post, post_id)

def get_posts_by_user(session: Session, user_id: int, offset: int = 0, limit: int = 10) -> List[Post]:
    """Filters the Post table by author_id (User Profile feed)."""
    statement = select(Post).where(Post.author_id == user_id).offset(offset).limit(limit)
    return list(session.exec(statement).all())