'''Control relay based on ambient temperature.'''
import time
import board
import busio
import digitalio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

# Tune to be adjusted.  Probably individual sensor specific.
# For a V2, possibly use tuning knobs?
TUNE = 3
TUNE2 = 1

# Set points
set_high = 70
set_low = 65

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

# Grab a pin for controlling relay
relay_pin = digitalio.DigitalInOut(board.D17)
relay_pin.direction = digitalio.Direction.OUTPUT
relay_pin.value = False
relay_active = False

# Do until the end of time:
while True:
    # Check the temperature
    ambient_temp = ((chan.voltage - .1) * 100 - 40) * 9 / 5 + 32 + TUNE
    circuit_temp = ((chan2.voltage - .1) * 100 - 40) * 9 / 5 + 32 + TUNE2

    # Print info
    print(datetime.now())
    print("Ambient Temp: " + str(ambient_temp))
    print("Circuitry temp: " + str(circuit_temp))

    # If Temperature >= set_high, turn on fans
    if ambient_temp >= set_high and circuit_temp <= 130 and relay_active is False:
        relay_pin.value = True
        print('Fan relay activated...')
        relay_active = True

    # If Temperature <= set_low, turn off fans
    if (ambient_temp <= set_low and relay_active is True) or (circuit_temp > 130 and relay_active is True):
        relay_pin.value = False
        print('Fan relay deactivated...')    
        relay_active = False

    # In addition to cutting off, hold off for 5 minutes for cooldown
    if circuit_temp > 130:
        print('Circuitry temp triggered 5 minute cooldown...')
        time.sleep(5)

    # Wait 1 minutes
    time.sleep(60)