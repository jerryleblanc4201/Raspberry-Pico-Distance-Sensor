# jerry leblanc for FIRST FRC Team 4201 11/10/23
# github Raspberry-Pico-Distance-Sensor 
# https://github.com/jerryleblanc4201/Raspberry-Pico-Distance-Sensor.git
# prev called distProx+LEDmatrix.py 

# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VCNL4010 proximity and light sensor.
# Will print the proximity and ambient light every second.
import time
import board
import digitalio
import busio
import adafruit_vcnl4010

#i2c = board.I2C()
#sensor = adafruit_vcnl4010.VCNL4010(i2c)

# You can optionally adjust the sensor LED current.  The default is 200mA
# which is the maximum value.  Note this is only set in 10mA increments.
# sensor.led_current_mA = 120  # Set 120 mA LED current

# You can also adjust the measurement frequency for the sensor.  The default
# is 390.625 khz, but these values are possible to set too:
# - FREQUENCY_3M125: 3.125 Mhz
# - FREQUENCY_1M5625: 1.5625 Mhz
# - FREQUENCY_781K25: 781.25 Khz
# - FREQUENCY_390K625: 390.625 Khz (default)
# sensor.frequency = adafruit_vcnl4010.FREQUENCY_3M125  # 3.125 Mhz

# import countLEDwithResetButton 

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
ledGP2 = digitalio.DigitalInOut(board.GP2)
ledGP2.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.GP3)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments
# Create the I2C interface.
i2c = busio.I2C(board.GP1, board.GP0)

# Create proximity sensor object 
sensor = adafruit_vcnl4010.VCNL4010(i2c)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c, address=0x70)
display.print(0)

# initial values
loopCount=0
MIN_PROXIMITY = 221
timeOn=0.1	# 0.5
timeOff=0.01  # 0.5

# Main loop runs forever printing the proximity and light level.
while True:
    loopCount = loopCount + 1
    proximity = round(sensor.proximity / 10)
    if proximity < MIN_PROXIMITY :
        proximity = 0
    # Proximity has no units and is a 16-bit
    # value.  The LOWER the value the further
    # an object from the sensor (up to ~200mm).
    print("Proximity: {0}".format(proximity))
    #ambient_lux = sensor.ambient_lux
    #print("Ambient light: {0} lux".format(ambient_lux))
    led.value = True
    print("Button: {0}".format(button.value))
    if button.value :
        ledGP2.value = True
        loopCount=0
    time.sleep(timeOn)
    led.value = False
    if proximity > 0 :
        ledGP2.value = True
    else :    
        ledGP2.value = False
    display.fill(0)
    display.print("{0}".format(proximity))
    time.sleep(timeOff)
    
