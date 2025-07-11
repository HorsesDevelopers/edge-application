import paho.mqtt.client as mqtt
import json

SOURCE_BROKER = "localhost"
SOURCE_PORT = 1883
SOURCE_TOPIC = "feed/command"

TARGET_BROKER = "localhost"
TARGET_PORT = 1884
TARGET_TOPIC = "feed/command"

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Mensaje recibido: {payload}")
    try:
        data = json.loads(payload)
        if data.get("pondId") == 1:
            target_client = mqtt.Client()
            target_client.connect(TARGET_BROKER, TARGET_PORT)
            target_client.publish(TARGET_TOPIC, msg.payload)
            target_client.disconnect()
            print("Mensaje reenviado al device.")
        else:
            print("pondId no es 1, no se reenvía.")
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(SOURCE_BROKER, SOURCE_PORT)
    client.subscribe(SOURCE_TOPIC)
    print(f"Escuchando en {SOURCE_BROKER}:{SOURCE_PORT} tópico '{SOURCE_TOPIC}'...")
    client.loop_forever()

if __name__ == "__main__":
    main()