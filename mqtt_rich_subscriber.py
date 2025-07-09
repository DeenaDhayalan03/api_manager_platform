import json
import uuid
from rich.console import Console
from rich.panel import Panel
from rich import box
import paho.mqtt.client as mqtt
from scripts.constants.app_configuration import settings

console = Console()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        console.print("[bold green]Connected to MQTT broker[/]")
        client.subscribe("tenant/+/warning")
        client.subscribe("tenant/+/credit-success")
        console.print("[bold cyan]Subscribed to:[/] tenant/+/warning, tenant/+/credit-success")
    else:
        console.print(f"[bold red]Connection failed with code {rc}[/]")

def on_message(client, userdata, msg):
    print(f"[SUBSCRIBER] Received message on topic: {msg.topic}")

    try:
        data = json.loads(msg.payload.decode())
        topic = msg.topic

        if "warning" in topic:
            console.print(
                Panel.fit(
                    f"[bold red]LOW CREDITS ALERT[/]\n"
                    f"[yellow]Tenant:[/] {topic.split('/')[1]}\n"
                    f"[yellow]Remaining:[/] {data.get('remaining')} credits\n"
                    f"[yellow]Message:[/] {data.get('message')}",
                    title="🔔 WARNING",
                    border_style="red",
                    box=box.ROUNDED,
                )
            )
        elif "credit-success" in topic:
            console.print(
                Panel.fit(
                    f"[bold green]CREDITS DEDUCTED[/]\n"
                    f"[yellow]Tenant:[/] {topic.split('/')[1]}\n"
                    f"[yellow]Used:[/] {data.get('used')} credits",
                    title="💰 CREDITS USED",
                    border_style="green",
                    box=box.ROUNDED,
                )
            )
        else:
            console.print(f"[grey]Unknown Topic: {topic}[/]")

    except Exception as e:
        console.print(f"[bold red]Error processing message: {e}[/]")


def run_rich_subscriber():
    client_id = f"{settings.MQTT_CLIENT_ID}-{uuid.uuid4()}"
    client = mqtt.Client(
        client_id=client_id,
        clean_session=settings.MQTT_CLEAN_SESSION,
    )

    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    console.print("[bold magenta]🔌 Connecting to MQTT...[/]")
    client.connect(settings.MQTT_BROKER_URL, settings.MQTT_PORT)
    client.loop_forever()

if __name__ == "__main__":
    run_rich_subscriber()
