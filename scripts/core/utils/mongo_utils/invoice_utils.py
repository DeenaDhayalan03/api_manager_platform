from scripts.core.utils.mongo_utils.db_connection import db
from datetime import datetime
from scripts.constants.app_configuration import settings


def generate_invoice(tenant_id: str, logs: list, total_credits: int) -> dict:
    invoice_doc = {
        "tenant_id": tenant_id,
        "total_credits_used": total_credits,
        "log_count": len(logs),
        "logs": logs,
        "generated_at": datetime.utcnow()
    }
    db[settings.INVOICES_COLLECTION].insert_one(invoice_doc)
    return invoice_doc


def get_invoices_by_tenant(tenant_id: str) -> list:
    return list(db[settings.INVOICES_COLLECTION].find({"tenant_id": tenant_id}))
