from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from web_app.models import Follow, ModelError, User


def follow_user(session: Session, follower_id: int, followed_id: int) -> Follow | ModelError:
    """
    Creates and persists a new Follow relationship.

    In case of success, the Follow table model is returned.
    In case of error a ModelError enum is returned.
    """
    # Prevent users from following themselves
    if follower_id == followed_id:
        return ModelError.CAN_NOT_FOLLOW_YOURSELF

    # Ensure the user being followed actually exists
    if not session.get(User, followed_id):
        return ModelError.USER_ID_NOT_FOUND

    db_follow = Follow(
        follower_id=follower_id,
        followed_id=followed_id
    )

    try:
        session.add(db_follow)
        session.commit()
        session.refresh(db_follow) # Load generated attributes (like ID and created_at)
        return db_follow

    except IntegrityError as e:
        # Rollback the transaction to keep the session in a clean state
        session.rollback()
        # Triggers if the unique constraint "unique_follower_followed" is violated
        return ModelError.ALREADY_FOLLOWING
        session.rollback()

    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR


def unfollow_user(session: Session, follower_id: int, followed_id: int) -> bool | ModelError:
    """
    Removes a Follow relationship between two users.

    Returns True if successfully deleted, or a ModelError.
    """
    # Look for the existing relationship before attempting deletion
    db_follow = get_follow_relationship(session, follower_id, followed_id)

    if not db_follow:
        return ModelError.FOLLOW_NOT_FOUND

    try:
        session.delete(db_follow)
        session.commit()
        return True
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR

# Returns the full Follow object (the database record) or None.
def get_follow_relationship(session: Session, follower_id: int, followed_id: int) -> Follow | None:
    """
    Returns a specific follow relationship if it exists, or None.
    """
    statement = select(Follow).where(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    )
    return session.exec(statement).first()

# Returns a simple boolean (True or False). It checks for existence and immediately converts the result to a truth value.
def is_following(session: Session, follower_id: int, followed_id: int) -> bool:
    """
    Checks if a follow relationship exists between two users.
    """
    return bool(get_follow_relationship(session, follower_id, followed_id)) # Convert object/None to True/False


def get_followed_users(session: Session, user_id: int) -> list[User]:
    """Returns a list of Users that the specified user is following."""
    statement = (
        select(User)
        .join(Follow, Follow.followed_id == User.id)
        .where(Follow.follower_id == user_id)
    )
    return list(session.exec(statement).all())