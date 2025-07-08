from scripts.core.utils.jwt_utils.jwt_handler import create_token
from scripts.constants.app_configuration import settings


def generate_access_token(user: dict) -> str:
    """
    Generate JWT access token.
    """
    username = user.get("username")
    tenant_id = user.get("tenant_id")
    role = user.get("role")

    if not username or not tenant_id or not role:
        raise ValueError("Missing fields in user payload: username, tenant_id, or role")

    return create_token(
        data={
            "sub": username,
            "tenant_id": tenant_id,
            "role": role,
            "type": "access"
        },
        expires_minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )


def generate_refresh_token(user: dict) -> str:
    """
    Generate JWT refresh token.
    """
    username = user.get("username")
    if not username:
        raise ValueError("Missing username for refresh token")

    return create_token(
        data={
            "sub": username,
            "type": "refresh"
        },
        expires_minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES  # optional: add separate setting
    )
