from fastapi import APIRouter, HTTPException, Form
from scripts.core.model.auth_models import RegisterRequest, LoginRequest, TokenResponse
from scripts.core.handler.auth_handler import AuthHandler
from scripts.constants.api_endpoints import APIEndpoints

router = APIRouter()


@router.post(APIEndpoints.REGISTER, response_model=TokenResponse)
def register_user(data: RegisterRequest):
    try:
        return AuthHandler.register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(APIEndpoints.LOGIN, response_model=TokenResponse)
def login_user(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        data = LoginRequest(username=username, password=password)
        return AuthHandler.login_user(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
