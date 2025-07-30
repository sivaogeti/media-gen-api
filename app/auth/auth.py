from fastapi import Request, HTTPException, status
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Replace with a more secure method later (e.g., from .env)
API_TOKEN = "my_secure_token_123"  # we can generate a random one using uuid or secrets

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token.replace("Bearer ", "") != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return request

security = HTTPBearer()

VALID_TOKENS = {"token123", "mysecuretoken"}  # Your valid tokens

def auth_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    if token not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    return token

