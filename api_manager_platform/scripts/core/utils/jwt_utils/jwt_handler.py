from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from scripts.constants.app_configuration import settings
from scripts.constants.api_endpoints import APIEndpoints

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=APIEndpoints.LOGIN)


def create_token(data: dict, expires_minutes: int) -> str:
    """
    Create JWT access or refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    """
    Decode and return the payload if token is valid.
    """
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        print(" JWT decode error:", str(e))
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to extract and validate user from token.
    """
    print(" Raw token:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    role = payload.get("role")

    print("Token Payload:", payload)

    if not username or not tenant_id or not role:
        raise credentials_exception

    return payload
