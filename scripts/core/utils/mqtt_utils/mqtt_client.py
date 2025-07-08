import asyncio
import paho.mqtt.client as mqtt
from scripts.constants.app_configuration import settings

mqtt_client = mqtt.Client(
    client_id=settings.MQTT_CLIENT_ID,
    clean_session=settings.MQTT_CLEAN_SESSION,
)

mqtt_client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code", rc)

def on_disconnect(client, userdata, rc):
    print("MQTT Disconnected with code", rc)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect


def connect_mqtt():
    mqtt_client.connect(
        host=settings.MQTT_BROKER_URL,
        port=settings.MQTT_PORT,
        keepalive=settings.MQTT_KEEPALIVE,
    )
    mqtt_client.loop_start()
