
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels =3
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
print(ORDER)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER)

i=0
while True:
	pixels[i]=(255,255,255)
	pixels.show()
	time.sleep(1)
	i=i+1
	if (i>4):
		i=0

