import dht
import json
import network
import socket
import utime

from ds18x20 import DS18X20
from machine import Pin
from onewire import OneWire

from sleep import deep_sleep
from wifi import init_wifi


def init_multicast():
    # Ensure AP wifi is disabled (see: https://github.com/micropython/micropython/issues/2198)
    network.WLAN(network.AP_IF).active(False)
    utime.sleep_ms(200)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def send_multicast(sock, data):
    buf = data.encode('utf-8')
    print("WRITE", buf)
    sock.sendto(buf, ('239.0.0.22', 3535))


def get_data_dht(pin_nr):
    pin = Pin(pin_nr)
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
    ds_pin = Pin(pin_nr)
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


def main(pin_nr):
    state = {'station': None, 'wifi': None}
    init_wifi(state)
    utime.sleep_ms(1000)

    sock = init_multicast()

    data = get_data_ds18b20(pin_nr)

    # only send when data is available
    if data is not None:
        # Publish the values via multicast
        send_multicast(sock, json.dumps(data))
    
    # Sleep so the socket gets flushed before going into deep sleep
    utime.sleep_ms(300)

    # Sleep for 30 seconds before restarting
    print("Going to sleep")
    deep_sleep(30*1000)
