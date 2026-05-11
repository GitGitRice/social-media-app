from web_app.models import Post, ModelError, User, Like
from sqlmodel import Session, select, desc
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def create_post(session: Session, db_post: Post) -> Post | ModelError:
    """
    Adds a PostCreate object to the db session and commits it.

    In case of success, the Post table model is returned.
    In case of error a ModelError enum is returned.
    """
    try:
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

    except IntegrityError as e:
        # Happens if the author_id does not exist in the User table (Foreign Key Constraint)
        print(f"IntegrityError: {e}")
        session.rollback()
        return ModelError.USER_ID_NOT_FOUND

    except ValidationError as e:
        # Happens if the post content doesn't meet the schema requirements
        print(f"ValidationError: {e}")
        session.rollback() # Add rollback for validation errors
        return ModelError.VALIDATION_ERROR
        
    

    except Exception as e:
        # Catch-all for other database issues
        print(f"Unexpected error: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR


def get_posts(session: Session, offset: int = 0, limit: int = 100) -> list[Post]:
    """
    Returns a list of Post table models from the db session with pagination.
    """
    statement = select(Post).offset(offset).limit(limit).order_by(desc(Post.created_at))
    users = session.exec(statement).all()
    return list(users)


def get_post_by_id(session: Session, post_id: int) -> Post | None:
    """
    Returns a single Post table model by its ID or None if not found.
    """
    return session.get(Post, post_id)


def get_post_author(session: Session, post_id: int) -> User | None:
    """
    Returns the author of a specific Post or None if the post or author was not found.
    """
    post = session.get(Post, post_id)
    if not post:
        return None
    return session.get(User, post.author_id)


def get_posts_by_user(session: Session, user_id: int, offset: int = 0, limit: int = 10) -> list[Post]:
    """
    Returns a list of Post table models filtered by a specific author_id.
    """
    statement = select(Post).where(Post.author_id == user_id).offset(offset).limit(limit)
    return list(session.exec(statement).all())


# needs another verification, so that not everyone can delete posts, if they know the id
# possibly users should only be able to delete their own posts
def delete_post_from_db(session: Session, post_id: int) -> bool:
    """
    Removes a Post record from the database.

    Returns True if successful, False if the post was not found.
    """
    db_post = session.get(Post, post_id)
    if not db_post:
        return False

    try:
        session.delete(db_post)
        session.commit()
        return True
    except Exception as e:
        print(f"Fehler beim Löschen: {e}")
        session.rollback()
        return False

def toggle_like_on_post (user_id: int | None, post_id: int | None, session: Session) -> ModelError | bool:

    if not user_id: return ModelError.USER_ID_NOT_FOUND
    if not post_id: return ModelError.POST_ID_NOT_FOUND

    try:
        user_exists = session.get(User, user_id)
        post_exists = session.get(Post, post_id)

        if not user_exists:
            return ModelError.USER_ID_NOT_FOUND
        if not post_exists:
            return ModelError.POST_ID_NOT_FOUND
        
        statement = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        like = session.exec(statement).first()
        if like:
            # unlike the post
            print ("unlike")
            session.delete(like)
            new_state = False
        else:
            # like the post
            print ("like")
            session.add(Like(user_id=user_id, post_id=post_id))
            new_state = True
        session.commit()
        return new_state
    
    except Exception as e:
        session.rollback()
        return ModelError.DATABASE_ERROR
    
    