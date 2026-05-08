from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, col

from web_app.models import Comment, ModelError, Post, User


def add_comment(
    session: Session,
    user_id: int,
    post_id: int,
    content: str,
) -> Comment | ModelError:
    """
    Creates and persists a new Comment record.

    In case of success, the Comment table model is returned.
    In case of error a ModelError enum is returned.
    """
    if not session.get(User, user_id):
        return ModelError.USER_ID_NOT_FOUND

    if not session.get(Post, post_id):
        return ModelError.POST_NOT_FOUND

    db_comment = Comment(
        user_id=user_id,
        post_id=post_id,
        content=content,
    )

    try:
        session.add(db_comment)
        session.commit()
        session.refresh(db_comment)
        return db_comment

    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR

    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        return ModelError.DATABASE_ERROR


def get_comments_for_post(session: Session, post_id: int) -> list[Comment]:
    """
    Returns all Comment records for a specific Post ordered by creation date.
    """
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(col(Comment.created_at))
    )
    return list(session.exec(statement).all())


def get_comment_count(session: Session, post_id: int) -> int:
    """
    Returns the total number of Comment records for a specific Post.
    """
    statement = select(func.count(col(Comment.id))).where(Comment.post_id == post_id)
    return session.exec(statement).one()
