import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn
import funcs
from datetime import datetime, timedelta

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,  GPIO.OUT)

DRY_VALUE = 37000
WET_VALUE = 23500
MEAN_MAX_VALUE = DRY_VALUE - WET_VALUE

announced_enough = False
announced_too_much = False
last_dry_announcement = datetime.now()

while True:
	moisture_percentage = (100 - max(min((((channel.value - WET_VALUE) / MEAN_MAX_VALUE) * 100), 100), 0))
	if not funcs.quiet_hours():
		if moisture_percentage < 20 and datetime.now() > last_dry_announcement + timedelta(minutes=15):
			announced_enough = False
			announced_too_much = False
			last_dry_announcement = datetime.now()
			funcs.pickRandomDry()
			#time.sleep(10)
		elif 20 < moisture_percentage < 40 and not announced_enough:
			print("enough")
			announced_enough = True
			announced_too_much = False
			funcs.pickRandomEnough()
			#time.sleep(10)
		elif moisture_percentage > 40 and not announced_too_much:
			announced_too_much = True
			funcs.pickRandomWet()
			#time.sleep(10)
	#print('Raw ADC Value: ', channel.value)
	#print('ADC Voltage: ' + str(channel.voltage) + 'V')
	print(f'Soil moisture: {moisture_percentage}%')
	time.sleep(1)

