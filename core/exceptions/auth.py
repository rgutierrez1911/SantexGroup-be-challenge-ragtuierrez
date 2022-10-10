from fastapi import HTTPException, status
from typing import Any, List, Optional, Dict


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="we_cannot_validate_the_credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_type_refresh_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="refresh_token_invalid",
    headers={"WWW-Authenticate": "Bearer"},
)

type_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="no_type_defined_for_this_token",
    headers={"WWW-Authenticate": "Bearer"},
)


invalid_jwt_token = HTTPException(
    status_code=420,
    detail="invalid_token",
    headers={"WWW-Authenticate": "Bearer"},
)


class PermitionException(HTTPException):
    def __init__(self,
                 status_code: int,
                 permitions: List[str] = [],
                 headers: Optional[Dict[str, Any]] = None
                 ) -> None:
        complete_detail = f"Missing permition from list {permitions}"

        super().__init__(status_code, complete_detail, headers)
