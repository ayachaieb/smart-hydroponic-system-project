# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import paho.mqtt.client as mqtt

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
verif=0
# The number of NeoPixels
num_pixels = 3

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
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
    verif=1
    light_up(0,0,0)
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

client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
#print(verif)
while verif==0:
        balayage()
        print(verif)
client.loop_forever()

