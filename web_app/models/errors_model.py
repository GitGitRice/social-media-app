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
    POST_ID_NOT_FOUND = "POST_ID_NOT_FOUND"

        # Errors related to Follow CRUD
    FOLLOW_NOT_FOUND = "FOLLOW_NOT_FOUND"
    CAN_NOT_FOLLOW_YOURSELF = "CAN_NOT_FOLLOW_YOURSELF"
    CAN_NOT_UNFOLLOW_YOURSELF = "CAN_NOT_UNFOLLOW_YOURSELF"
    ALREADY_FOLLOWING = "ALREADY_FOLLOWING"


    @property
    def http_status(self) -> int:
        """Maps model errors to HTTP status codes."""
        mapping = {
            self.VALIDATION_ERROR: 422,
            self.USER_NAME_ALREADY_EXISTS: 400,
            self.USER_NAME_NOT_FOUND: 404,
            self.USER_ID_NOT_FOUND: 404,
            self.FOLLOW_NOT_FOUND: 404,
            self.CAN_NOT_FOLLOW_YOURSELF: 400,
            self.CAN_NOT_UNFOLLOW_YOURSELF: 400,
            self.ALREADY_FOLLOWING: 409, # Conflict, as the resource (follow) already exists
            self.POST_ID_NOT_FOUND: 404,
            self.DATABASE_ERROR: 500,
        }
        return mapping.get(self, 500)
    
