from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum

# --- Existing User Models ---

class UserBase (SQLModel):
    """
    A data model with the basic user attributes.
    """
    user_name : str = Field(unique=True)
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None


class User (UserBase, table=True):
    """
    A table model with the columns stored in db.
    """
    id: int | None = Field (default=None, primary_key=True) # need to be optional due to SQLModel inner workings.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)
    )
    # hashed_password : str
    # RELATIONSHIP: Link User to Posts
    posts: List["Post"] = Relationship(back_populates="author")

class UserCreate (UserBase):
    """
    A data model with the additional attributes during user creation.
    """
    # password: str
    pass


class UserRead (UserBase):
    """
    A data model with the additonal attributes to be returned for a user.
    """
    id: int
    created_at: datetime


class PostBase(SQLModel):
    content: str
    

class Post(PostBase, table=True):
    id: int | None = Field (
        default=None,
        primary_key=True
    )
    # Verlinkung mit User.id
    author_id: int = Field(foreign_key="user.id")
    
    # Verlinkt Post zurück mit Author
    author: User = Relationship(back_populates="posts")
    
    
class PostCreate(PostBase):
    author_id: int  

class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime


class UserPatch (SQLModel):
    """
    A data model with the attributes to be used for PATCH routes.
    """
    user_name : str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None
    password: str | None = None


class ModelError(str, Enum):
    """
    Collects the different error codes when working with table models.
    """
    VALIDATION_ERROR = "VALIDATION_ERROR" #errors caused by Pydantic evaluation.
    USER_NAME_ALREADY_EXISTS = "USER_NAME_ALREADY_EXISTS"
    DATABASE_ERROR = "DATABASE_ERROR"
