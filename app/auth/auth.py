#from fastapi import Depends, HTTPException, status
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from fastapi import Security
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

#security = HTTPBearer()

from fastapi import Header, HTTPException, Depends

VALID_TOKENS = ["my_secure_token_123"]  # or load from file/db/env

def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    # Replace with your actual logic (static check shown here)
    if token != "my_secure_token_123":
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid or expired token"
        )

