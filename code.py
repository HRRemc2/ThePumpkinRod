import time   
import board
import digitalio
import neopixel
import adafruit_veml7700


def LED_setup():
    global NUM_PIXELS
    global delay
    global which_pixel
    global power_pin
    global pixels
    global direction
#Variable Initialization
    
    NUM_PIXELS = 30
    delay =0.1
    which_pixel = 0
    
    power_pin = digitalio.DigitalInOut(board.EXTERNAL_POWER)
    power_pin.direction = digitalio.Direction.OUTPUT
    power_pin.value = True
    
    pixels = neopixel.NeoPixel(
        board.EXTERNAL_NEOPIXELS,
        NUM_PIXELS, brightness=10,
        auto_write=False
    )
    
    direction= 1
    
    
def LED_loop():
    global which_pixel
    global direction


    pixels.fill((0, 0, 0))
    
# Turn ON only one pixel
    pixels[which_pixel] = (0*(which_pixel/NUM_PIXELS), 0*(1-which_pixel/NUM_PIXELS),150) # The(R,G,B)
# Update the strip
    pixels.show()

    time.sleep(delay)

# Increment which pixel is ON and check for the end
    which_pixel = which_pixel + direction

    if which_pixel >= NUM_PIXELS - 1:
        direction = -1
    if which_pixel <= 0:
        direction = 1
        
def luxSensor_setup():
    global i2c
    global luxSensor

    i2c = board.I2C()
    luxSensor = adafruit_veml7700.VEML7700(i2c)


def luxSensor_loop():
    print("Ambient light:", luxSensor.light)
    time.sleep(0.1)


def lux_LED_check():
    global LED_fire_color_chnl_1


    LED_fire_color_chnl_1 = (255, 0, 0)
    LED_fire_color_chnl_2 = (255, 0, 0)
    LED_fire_color_chnl_3 = (255, 0, 0)
    LED_fire_color_chnl_4 = (255, 0, 0)


    if luxSensor.light < 100:
        pixels.fill((LED_fire_color_chnl_1))
    else:
        pixels.fill((0, 0, 0))
    pixels.show()

    

    
LED_setup()
luxSensor_setup()

while True:
    #LED_loop()
    luxSensor_loop()
    lux_LED_check()
