import smbus
import time

# Constants taken from the datasheet

DEVICE = 0x23     # Default device I2C address, use i2cdetect -y 1 on the RPi in the command window to verify

POWER_DOWN = 0x00 # No active state
POWER_ON = 0x01   # Power on
RESET = 0x07      # Reset data register value

ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = smbus.SMBus(1)

def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2  # convert 2 bytes of data to decimal
    return (result)

def readLight(addr = DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

while True:

    lightLevel = readLight()

    if (lightLevel <= 0.01):    # quarter moon
        print('too dark')
    elif (lightLevel <= 10):    # twilight
        print('dark')
    elif (lightLevel <= 500):   # residential indoor lighting
        print('medium')
    elif (lightLevel <= 25000): # daylight
        print('bright')
    elif (lightLevel <= 65535): # direct sunlight, 65535 is the top of the operating range of the sensor
        print('too bright')

    #print('Light Level :' + format(lightLevel,'.2f') + ' lx')  # uncomment this print statement to check the light levels being recorded
    time.sleep(0.5)