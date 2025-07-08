from scripts.core.utils.mongo_utils.summary_utils import generate_usage_summary

def get_usage_summary_handler(current_user: dict):
    tenant_id = current_user["tenant_id"]
    return generate_usage_summary(tenant_id)
