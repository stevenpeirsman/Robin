import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from Log import log

load_dotenv()
BROKER_IP = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

def say_hello():
    payload = {
        "id": "proximity_greeting",
        "type": "speech",
        "blockInfo": {
            "blocking": False,
            "initiated": True,
            "text": "Hallo! Leuk je te zien!",
            "speechLanguage": "nl-NL",
            "speed": 100,
            "speaker": "nl-NL-Standard-A"
        }
    }

    client = mqtt.Client()
    client.connect(BROKER_IP, PORT, 60)
    client.loop_start()
    log("Sending greeting via MQTT")
    client.publish(TOPIC, json.dumps(payload), qos=1)
    client.loop_stop()
    client.disconnect()
