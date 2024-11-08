
# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import paho.mqtt.client as mqtt

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

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
    time.sleep(1)


def on_message(client, userdata, msg):
    print(f'{msg.topic}')
    print(msg.payload)
    if  (msg.topic=="room1/connected") :
        light_up(0,255,0)
    if  (msg.topic=="room1/disconnect") :
        light_up(255,0,0)  
    else :
        light_up(0,0,255)


def on_connect(client, userdata, flags, rc):
    print(f"Connected  with result code {rc}")
    client.subscribe("greeny/#")

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()