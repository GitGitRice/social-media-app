from enum import Enum


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

    # Errors related to post CRUD
    POST_NOT_FOUND = "POST_NOT_FOUND"
    AUTHOR_NOT_FOUND = "AUTHOR_NOT_FOUND" # In case author_id is invalid
