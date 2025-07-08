def get_low_credit_topic(tenant_id: str) -> str:
    return f"tenant/{tenant_id}/warning"

def get_credit_success_topic(tenant_id: str) -> str:
    return f"tenant/{tenant_id}/credit-success"
