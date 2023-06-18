import RPi.GPIO as GPIO
import board
import busio
# import Adafruit_DHT
import adafruit_dht     # pip3 install adafruit-circuitpython-dht
import adafruit_sgp30   # pip3 install adafruit-circuitpython-sgp30 

from time import sleep

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c, 0x58)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius=22.1, relative_humidity=44)

dht = adafruit_dht.DHT11(board.D10)

BUZZER  = 9
LED     = 11
#LIGHT   = 17
#signal  = 0

#DHT11   = dht11()

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(BUZZER , GPIO.OUT)
  GPIO.setup(LED    , GPIO.OUT)
#  GPIO.setup(LIGHT  , GPIO.IN )
#  signal = not GPIO.input(LIGHT)
  return

def main():
  try:
    elapsed_sec = 0
    init()
#    global signal

    while True:
#      if GPIO.input(LIGHT) != signal:
#        if not GPIO.input(LIGHT):
#          print('\u263e')   # dark
#        else:
#          print('\u263c')   # light
#      signal = GPIO.input(LIGHT)

#      humidity, temperature = DHT11.read()
      try:
        temperature = dht.temperature
        humidity    = dht.humidity
        if humidity is not None and temperature is not None:
          print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
      except RuntimeError as error:
        sleep(0.5)
        continue

      print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
      elapsed_sec += 1
      if elapsed_sec > 10:
        elapsed_sec = 0
        print(
          "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
          % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
        )

      GPIO.output(BUZZER, GPIO.LOW)
      GPIO.output(LED, GPIO.LOW)
      sleep(1.5)
      GPIO.output(BUZZER, GPIO.HIGH)
      GPIO.output(LED, GPIO.HIGH)
      sleep(0.5)
  except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)

if __name__ == "__main__":
  main()
