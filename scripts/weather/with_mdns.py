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

    "controller_ip": None,
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


def setup_controller(hostname='weather-probe-controller'):
    global state

    ip = socket.getaddrinfo('weather-controller.local', 80)

    state['controller_ip'] = ip
    
    print("found controller in", state['controller_ip'])



def no_controller_link():
    # TODO: Also ping it to detect when link to ip is down

    return not state['controller_ip']


def loop():
    global state

    while True:
        if state['station'] is None or not state['station'].isconnected():
            init_wifi()
            utime.sleep_ms(300)
            continue

        try:
            if no_controller_link():
                setup_controller()

        except Exception as e:
            raise e

        else:
            print("sending packets to", state['controller_ip'])

        utime.sleep_ms(2000)


if __name__ == '__main__':
    loop()
