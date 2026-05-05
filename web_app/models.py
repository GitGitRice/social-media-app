from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from enum import Enum


#--------------------------- User Models ----------------------------
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
    hashed_password : str


class UserCreate (UserBase):
    """
    A data model with the additional attributes during user creation.
    """
    password: str
    pass


class UserRead (UserBase):
    """
    A data model with the additonal attributes to be returned for a user.
    """
    id: int
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


#--------------------------- Model Errors ----------------------------

class ModelError(str, Enum):
    """
    Collects the different error codes when working with table models.
    """
    VALIDATION_ERROR = "VALIDATION_ERROR" #errors caused by Pydantic evaluation.
    DATABASE_ERROR = "DATABASE_ERROR" # general database errors

    # Errors related to user CRUD
    USER_NAME_ALREADY_EXISTS = "USER_NAME_ALREADY_EXISTS"
    USER_NAME_NOT_FOUND = "USER_NAME_NOT_FOUND"
    USER_ID_NOT_FOUND = "USER_ID_NOT_FOUND"
