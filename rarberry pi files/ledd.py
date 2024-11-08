from threading import Thread
import time
import board
import neopixel
import paho.mqtt.client as mqtt

pixel_pin = board.D18
verif=0
# The number of NeoPixels
num_pixels = 3
check = False
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER
)
client = mqtt.Client()
def light_up(a,b,c):
    pixels.fill((a,b,c))
    pixels.show()
  


def on_message(client, userdata, msg):
    print(f'{msg.topic}')
    print(msg.payload)
    if  (msg.topic=="room1/connected") :
        light_up(0,255,0)
        time.sleep(1)
        print("connectedgreeny")
    if  (msg.topic=="room1/disconnect") :
        light_up(255,0,0)  
        time.sleep(1)
    if ("sensor" in msg.topic) :
        print("condition")
        light_up(255,255,255)
        pixels.fill((0,0,0))
        pixels.show()

def on_connect(client, userdata, flags, rc):
    print(f"Connected  with result code {rc}")
    client.subscribe("room1/#")

def balayage ():
    for i in range (0,3,1):
        pixels.fill((255,255,255))
        pixels[i]=(0,0,255)
        time.sleep(1)
        pixels.show()

def state_0():
    print ("funn1 started")
    while True:
        if check:
            balayage()
            print ("led on")
            break
    

def started_receiving_messages():
    global check
    print ("func2 started")
    check = True
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.loop_forever()

if __name__ == '__main__':
    Thread(target = state_0).start()
    Thread(target = started_receiving_messages).start()