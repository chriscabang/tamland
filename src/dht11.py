import os
import RPi.GPIO as GPIO
#import configparser
import adafruit_dht     # pip3 install adafruit-circuitpython-dht
import socket

from jproperties import Properties
from time import sleep

#DHT_PIN = 10
#dht = adafruit_dht.DHT11(DHT_PIN)

#server_ip     = 'localhost'
#server_port   = 9999

config = Properties()
with open("." + os.path.splitext(os.path.basename(__file__))[0], 'rb') as config_file:
  config.load(config_file)

#print(config.get("server").data)
dht = adafruit_dht.DHT11(int(config.get("dht11_pin").data))

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
#  GPIO.setup(DHT_PIN, GPIO.IN)
  return

def main():
  try:
    init()
    temperature = dht.temperature
    humidity    = dht.humidity
    while True:
      try:
        # Process only when there is change
        if dht.temperature != temperature or dht.humidity != humidity:
          temperature = dht.temperature
          humidity    = dht.humidity
          if humidity is not None and temperature is not None:
            data="Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
              client_socket.connect(
                (config.get("server").data,
                 int(config.get("port").data))
              )
              client_socket.sendall(data.encode())
            except ConnectionRefusedError:
              print("Connection refused, server unavailable")
              print(data)
            finally:
              client_socket.close()

          sleep(2.3)
      except RuntimeError as error:
        sleep(0.7)
        continue

  except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)

if __name__ == "__main__":
  main()
