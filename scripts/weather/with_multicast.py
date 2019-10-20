import dht
import network
import socket
import utime

from machine import Pin


sensor = dht.DHT11(Pin(15))

state = {
    "temp": None,
    "hum": None,

    "wifi": ('ssid', 'pw'),
    "station": None,

    'sock': None,
}


def connect_wifi():
    global state

    print("Connecting to wifi network {}".format(state["wifi"][0]))
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(*state["wifi"])

    while not station.isconnected():
        pass

    station.ifconfig()

    state['station'] = station


def init_wifi():
    global state

    print("loading wifi info from wifi.txt")

    with open('wifi.txt', 'r') as h:
        lines = h.read().splitlines()
        wifi_info = tuple([line.strip() for line in lines])

        state["wifi"] = (wifi_info[0], wifi_info[1])

    connect_wifi()


def measure():
    global state

    sensor.measure()

    state["temp"] = sensor.temperature()
    state["hum"] = sensor.humidity()


def send_multicast(data):
    if not state['sock']:
        state['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state['sock'].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    state['sock'].sendto(data.encode('utf-8'), ('239.0.0.22', 3535))


def loop():
    global state

    while True:
        if state['station'] is None or not state['station'].isconnected():
            init_wifi()
            utime.sleep_ms(300)
            continue

        # Get current temperature and humidity
        measure()

        # Publish the values via multicast
        send_multicast("Temperature: %d and Humidity: %d%%" % (state["temp"], state["hum"]))

        utime.sleep_ms(2000)


if __name__ == '__main__':
    loop()
