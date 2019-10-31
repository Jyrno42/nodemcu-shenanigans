import dht
import json
import machine
import network
import socket
import utime

from ds18x20 import DS18X20
from onewire import OneWire

from controller import init_link, post_data
from sleep import deep_sleep


def get_data_dht(pin_nr):
    pin = machine.Pin(pin_nr)
    sensor = dht.DHT11(pin)

    # Get current temperature and humidity
    sensor.measure()

    # sleep a bit for the result to be reliable
    utime.sleep_ms(200)

    return {
        'temperature': sensor.temperature(),
        'humidity': sensor.humidity(),
    }


def get_data_ds18b20(pin_nr):
    ds_pin = machine.Pin(pin_nr)
    ds_sensor = DS18X20(OneWire(ds_pin))

    roms = ds_sensor.scan()

    if not roms:
        return None

    ds_sensor.convert_temp()
    utime.sleep_ms(750)  # give enough time to convert the temperature

    temperature = None

    for rom in roms:
        temperature = ds_sensor.read_temp(rom)

    return {
        'temperature': temperature,
        'humidity': None
    }


try:
    pin_nr = 4
    value = get_data_ds18b20(pin_nr)
    timestamp = '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.0Z'.format(*utime.localtime())

    addr = init_link('temperature-1')
    post_data(addr, '/api/temperature', data={'value': value['temperature'], 'timestamp': timestamp})

except Exception as e:
    print('Error')
    print(e)
    machine.reset()

sleep_delay = 60 * 1000

# Sleep for 30 seconds before restarting
print("Going to sleep")
deep_sleep(sleep_delay)
