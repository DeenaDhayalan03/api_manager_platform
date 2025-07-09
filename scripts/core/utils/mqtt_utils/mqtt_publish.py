import json
from scripts.core.utils.mqtt_utils.mqtt_client import mqtt_client
from scripts.core.utils.mqtt_utils import mqtt_topics
from scripts.core.utils.mqtt_utils.mqtt_publisher_client import publish_mqtt_message


def publish_low_credit_alert(tenant_id: str, remaining_credits: int, message: str = None):
    topic = mqtt_topics.get_low_credit_topic(tenant_id)

    payload = {
        "type": "low_credits",
        "remaining": remaining_credits,
        "message": message or f"Low credit alert: only {remaining_credits} credits left."
    }

    mqtt_client.publish(topic, json.dumps(payload), retain=False)
    print(f"[MQTT] Published low credit alert to {topic}: {payload}")


def publish_credit_success(tenant_id: str, credits_used: int):
    topic = mqtt_topics.get_credit_success_topic(tenant_id)
    payload = {
        "type": "credit_deducted",
        "used": credits_used
    }

    publish_mqtt_message(topic, payload)

