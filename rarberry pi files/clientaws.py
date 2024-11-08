import paho.mqtt.client as mqtt
import os
import uuid
import ssl
import time

# AWS IoT Core details
aws_endpoint = "agxdrdba1l1ch-ats.iot.eu-west-3.amazonaws.com"  # Example: "a3k7odshaiipe8-ats.iot.us-east-1.amazonaws.com"
port = 8883
topic = "test/topic"
# Paths to the certificate and key files
ca_path = './rootCA.pem'
cert_path ='./certificate.pem.crt'
key_path = './private-key.pem.key'

# Specify the file path
file_path = "/home/ayach/code/uuid.txt"
verif=0
client = mqtt.Client()
clientaws=mqtt.Client()
if os.path.exists(file_path):
	print("existing file")


f = open(file_path, "r")
uu =f.readline()
base ="greeny/unit/"+uu+"/room1/"

ph_topic = base+"ph/sensor"
ec_topic = base +"ec/sensor"
humidity_topic = base +"humidity/sensor"
temperature_topic = base+"temperature/sensor"
water_temp_topic = base+"waterTemp/sensor"
air_quality_topic = base+"co2/sensor"
water_Level_topic = base+"waterLevel/sensor"
ph_modif =base+"ph/command"
ec_modif = base+"ec/command"
watermodif = base+"waterLevel/command"
connection_topic = base+"status"
print(base)
def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("room1/ph/sensor")
        client.subscribe("room1/ec/sensor")
        client.subscribe("room1/humidity/sensor")
        client.subscribe("room1/temperature/sensor")
        client.subscribe("room1/water_temp/sensor")
        client.subscribe("room1/air_quality/sensor")
        client.subscribe("room1/waterLevel/sensor")
        client.subscribe("room1/connected")
        client.subscribe("room1/disconnect")
        client.subscribe("greeny/unit/#")


# The callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f'{msg.topic}')
    print(msg.payload)
    if  (msg.topic=="room1/ph/sensor") :
        clientaws.publish(ph_topic,msg.payload)
    if  (msg.topic=="room1/ec/sensor") :
        clientaws.publish(ec_topic,msg.payload)
    if  (msg.topic=="room1/humidity/sensor") :
        clientaws.publish(humidity_topic,msg.payload)
    if  (msg.topic=="room1/temperature/sensor") :
        clientaws.publish(temperature_topic,msg.payload)
    if  (msg.topic=="room1/water_temp/sensor") :
        clientaws.publish(water_temp_topic,msg.payload)
    if  (msg.topic=="room1/air_quality/sensor") :
        clientaws.publish(air_quality_topic,msg.payload)
    if  (msg.topic=="room1/waterLevel/sensor") :
        clientaws.publish(water_Level_topic,msg.payload)
    if  (msg.topic==ph_modif) :
        clientaws.publish("room1/ph/command",msg.payload)
    if  (msg.topic==ec_modif) :
        clientaws.publish("room1/ec/command",msg.payload)
    if	(msg.topic==watermodif):
        clientaws.publish("room1/waterLevel/command",msg.payload)
    if  (msg.topic =="room1/connected"):
        print("connect room11")
        clientaws.publish(connection_topic ,"{room:room1,status:connected}")
    if  (msg.topic=="room1/disconnect"):
#        print("disconnected")
        clientaws.publish( base+"status", "{room_number:1 ,state:disconnected}")

def on_connectaws(client, userdata, flags, rc):
    print(f"Connected  to aws with result code {rc}")

def on_messageaws(client, userdata, msg):
    print(f'{msg.topic}')
    print(msg.payload)

client.on_connect = on_connect
client.on_message = on_message

clientaws.on_connect = on_connectaws
clientaws.on_message = on_messageaws

# Set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('greeny/unit/status', b'{"status": "Off"}')


client.connect("localhost", 1883)
# Create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
# Configure TLS/SSL connection
clientaws.tls_set(ca_certs=ca_path,certfile=cert_path,keyfile=key_path,tls_version=ssl.PROTOCOL_TLSv1_2)
# Connect to the AWS IoT Core MQTT broker
clientaws.connect(aws_endpoint, port, keepalive=60)
# Loop to keep the connection alive and publish messages

if verif==1 :
	clientaws.publish("greeny/unit/birth" , str(uu))
	print("theuuid is sent")



# Set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash

clientaws.loop_forever()
