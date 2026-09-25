import time   
import board
import digitalio
import neopixel
import adafruit_veml7700
import random
import audiobusio
import audiocore
import audiomixer



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

    red_chnl_3: int
    green_chnl_3: int

    red_chnl_3 = random.randint(100, 255)
    green_chnl_3 = random.randint(0, 30)


    LED_fire_color_chnl_1 = (255, 0, 0)
    LED_fire_color_chnl_2 = (255, 0, 0)
    LED_fire_color_chnl_3 = (red_chnl_3, green_chnl_3, 0)
    LED_fire_color_chnl_4 = (0, 0, 0)


    if luxSensor.light < 100:
        pixels.fill((LED_fire_color_chnl_3))
    else:
        pixels.fill((0, 0, 0))
    pixels.show()


def Sound_setup():
    global power
    global i2s
    global wave_file
    global wave
    global mixer

    # SFX channels
    global SFX_1
    global SFX_2
    global SFX_3
    global SFX_4
    global SFX_5

    SFX_1 = "Labyrinth.wav"

    # EXTERNAL_POWER is already set up in LED_setup()
    power = power_pin

    wave_file = open(SFX_1, "rb")
    wave = audiocore.WaveFile(wave_file)

    mixer = audiomixer.Mixer(
        voice_count=1,
        sample_rate=wave.sample_rate,
        channel_count=1,
        bits_per_sample=wave.bits_per_sample,
        samples_signed=True
    )

    mixer.voice[0].level = 0.5

    i2s = audiobusio.I2SOut(
        board.I2S_BIT_CLOCK,
        board.I2S_WORD_SELECT,
        board.I2S_DATA
    )

    i2s.play(mixer)



def Sound_loop():
    global Is_audio_playing

    Is_audio_playing = False

    i2s.play(mixer)


#Volume, goes from 0 to 1
    mixer.voice[0].level = 0.5

    print("Playing Audio")
    mixer.voice[0].play(wave)

    if mixer.voice[0].playing:
        Is_audio_playing = True
    else:
        Is_audio_playing = False
        wave_file.close




LED_setup()
luxSensor_setup()
Sound_setup()

while True:
    #LED_loop()
    luxSensor_loop()
    lux_LED_check()
    Sound_loop()
    time.sleep(3)


