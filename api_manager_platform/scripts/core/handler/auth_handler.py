from datetime import datetime, timedelta
from scripts.core.model.auth_models import RegisterRequest, LoginRequest
from scripts.core.utils.mongo_utils.user_utils import get_user_by_username, create_user
from scripts.core.utils.mongo_utils.plan_utils import get_plan_by_name
from scripts.core.utils.mongo_utils.subscription_utils import create_subscription
from scripts.core.utils.jwt_utils.password_handler import hash_password, verify_password
from scripts.core.utils.jwt_utils.token_generator import generate_access_token
from scripts.constants.app_configuration import settings
import uuid


class AuthHandler:

    @staticmethod
    def register_user(data: RegisterRequest) -> dict:
        existing_user = get_user_by_username(data.username)
        if existing_user:
            raise ValueError("Username already exists")

        if data.role == "admin":
            if not data.admin_setup_token or data.admin_setup_token != settings.ADMIN_SETUP_TOKEN:
                raise ValueError("Unauthorized to create admin user")

        plan = get_plan_by_name(data.plan_name)
        if not plan:
            raise ValueError("Selected plan does not exist")
        plan.pop("_id", None)

        tenant_id = str(uuid.uuid4())
        duration_days = plan.get("duration_days", 30)

        user_doc = {
            "username": data.username,
            "password": hash_password(data.password),
            "role": data.role,
            "tenant_id": tenant_id,
            "service_name": data.service_name,
            "plan_name": data.plan_name,
            "credits": plan.get("credits"),
            "plan_expiry": datetime.utcnow() + timedelta(days=duration_days)
        }

        created_user = create_user(user_doc)

        create_subscription(
            tenant_id=tenant_id,
            plan_name=data.plan_name,
            service_name=data.service_name,
            duration_days=duration_days
        )

        token = generate_access_token(created_user)
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    def login_user(data: LoginRequest) -> dict:
        user = get_user_by_username(data.username)
        if not user or not verify_password(data.password, user["password"]):
            raise ValueError("Invalid username or password")

        token = generate_access_token(user)
        return {"access_token": token, "token_type": "bearer"}
