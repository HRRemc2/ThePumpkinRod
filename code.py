import time   
import board
import digitalio
import neopixel   

# # The total number of pixels on the strip
NUM_PIXELS = 30
# Specify a time delay
delay =0.1
# Which pixel to turn on?
which_pixel = 0
# Need to enable the neopixel terminals
power_pin = digitalio.DigitalInOut(board.EXTERNAL_POWER)
power_pin.direction = digitalio.Direction.OUTPUT
power_pin.value = True
# Define the neopixel strip
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, NUM_PIXELS, brightness=10, auto_write=False)
# The infinite loop
which_pixel = 0
direction= 1
while True:
# Turn everything OFF
    pixels.fill((0, 0, 0))
# Turn ON only one pixel
    pixels[which_pixel] = (0*(which_pixel/NUM_PIXELS), 0*(1-which_pixel/NUM_PIXELS),150) # The(R,G,B)
# Update the strip
    pixels.show()
# Delay a bit
    time.sleep(delay)
# Increment which pixel is ON and check for the end
    which_pixel = which_pixel + direction

    if which_pixel >= NUM_PIXELS - 1:
        direction = -1
    if which_pixel <= 0:
        direction = 1
    
    

import time
import board
import adafruit_veml7700
# Initialize the i2c and sensor
i2c = board.I2C()
luxSensor = adafruit_veml7700.VEML7700(i2c)
# The infinite loop
while True:
    print("Ambient light:", luxSensor.light)
    time.sleep(0.1)
