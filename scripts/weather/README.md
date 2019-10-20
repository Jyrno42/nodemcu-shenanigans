# Just weather station things

ESP32 (IO15 is the data pin)

**refs:**

https://raw.githubusercontent.com/mcauser/micropython-tm1637
https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/

## DHT11 + 4 digit lcd weather station

code: [with_4digit_lcd.py](./with_4digit_lcd.py)

## multicast pattern

Deploy the [with_multicast.py](./with_multicast.py) to the ESP32 and start [multicast_server.py](./multicast_server.py) on your PC. You should 
start seeing the temperature values inside the python console.

## Controller/probe pattern

With MDNS for controller lookup (needs manually built firmware for ESP32 since mdns support is not yet in a stable release). 

The plan is to have multiple battery powered probes running on ESP32/ESP8266 and a single "controller" that has dedicated 
power. All of the devices are on the same network. The probes take their measurements, push the data to controller and then 
go into deep sleep. After a delay they wake up do it again. If possible, the probes should also monitor their own battery level.

The controller will most likely be a Rasperry Pi based SCU which will run a sink for probe events and maybe a dashboard for
statistics.
