'''Control relay based on ambient temperature.'''
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Tune to be adjusted.  Probably individual sensor specific.
TUNE = 8

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

# Do until the end of time:
while True:
    # Check the temperature
    rough_temp = ((chan.voltage - .1) * 100 - 40) * 9 / 5 + 32 + TUNE

    # If Temperature >= 75, turn on fans
    # TODO: Implement turn on relay

    # If Temperature <= 70, turn off fans
    # TODO: Implement turn off relay

    # Print info
    print("I live!")
    print(rough_temp)

    # Wait 1 minutes
    time.sleep(60)
