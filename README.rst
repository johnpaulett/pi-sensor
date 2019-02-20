==================
pi-sensor platform
==================

sudo apt-get install -y python3-pip python3-virtualenv virtualenv python3-gpiozero i2c-tools
virtualenv --python=python3 env
env/bin/pip3 install Adafruit_DHT adafruit-circuitpython-bmp3xx adafruit-circuitpython-sgp30 adafruit-circuitpython-tsl2591 prometheus_client

# adafruit-circuitpython-dht

I2C


https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
Address List: https://learn.adafruit.com/i2c-addresses/the-list

::
   sudo i2cdetect -y 1

0 for older boards

Sensors
=======

DHT22 - Humidity & Temperature
------------------------------

https://learn.adafruit.com/dht
https://www.adafruit.com/product/385

https://github.com/adafruit/Adafruit_Python_DHT
https://github.com/adafruit/Adafruit_CircuitPython_DHT


BMP388 - Precision Barometric Pressure and Altimeter
----------------------------------------------------

https://www.adafruit.com/product/3966

https://github.com/adafruit/Adafruit_CircuitPython_BMP3XX

Older BMP085: https://learn.adafruit.com/bmp085
https://www.mouser.com/pdfdocs/BST-BMP388-DS001-01.pdf

i2c Address: 0x77

SGP30 -  VOC and eCO2 Air Quality Sensor
----------------------------------------

https://www.adafruit.com/product/3709
https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/
https://circuitpython.readthedocs.io/projects/sgp30/en/latest/

i2c Address: 0x58 (can not be changed)

https://learn.adafruit.com/adafruit-tsl2591

TSL2591 - Luminosity
--------------------

https://www.adafruit.com/product/1980
https://learn.adafruit.com/adafruit-tsl2591
https://circuitpython.readthedocs.io/projects/tsl2591/en/latest/
i2c Address: 0x29

Old Sensors
============


MCP9808 - High Accuracy I2C Temperature Sensor
----------------------------------------------

pip install adafruit-circuitpython-mcp9808 

https://www.adafruit.com/product/1782
https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide
https://circuitpython.readthedocs.io/projects/mcp9808/en/latest/

i2c Address: 0x18

TSL2561 - Luminosity
--------------------

pip install adafruit-circuitpython-tsl2561
https://www.adafruit.com/product/439
https://learn.adafruit.com/tsl2561/overview
https://circuitpython.readthedocs.io/projects/tsl2561/en/latest/

i2c Address: 0x39


Fritzing
========

https://github.com/adafruit/Fritzing-Library
