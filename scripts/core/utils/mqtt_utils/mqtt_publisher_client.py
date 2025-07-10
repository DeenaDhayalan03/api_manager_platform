import json
import paho.mqtt.client as mqtt
from scripts.constants.app_configuration import settings

def publish_mqtt_message(topic: str, payload: dict):
    try:
        client = mqtt.Client()
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        client.connect(settings.MQTT_BROKER_URL, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
        client.loop_start()

        client.publish(topic, json.dumps(payload), retain=True)
        print(f"[MQTT] Published to {topic}: {payload}")

        client.loop_stop()
        client.disconnect()

    except Exception as e:
        print(f"[MQTT] Failed to publish to {topic}: {e}")