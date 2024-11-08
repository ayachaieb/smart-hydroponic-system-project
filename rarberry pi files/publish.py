import time 
import paho.mqtt.client as mqtt
topic="greeny"
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client= mqtt.Client()
client.on_connect=on_connect
#client.on_message=on_message
client.connect("localhost", 1883)
client.publish(topic,"message")
client.loop_forever()
