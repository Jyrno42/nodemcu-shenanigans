import network
import utime


def connect_wifi(state):
    print("Connecting to wifi network {}".format(state["wifi"][0]))

    # Ensure AP wifi is disabled (see: https://github.com/micropython/micropython/issues/2198)
    network.WLAN(network.AP_IF).active(False)
    utime.sleep_ms(200)

    # Connect to wifi network as a client
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(*state["wifi"])

    while not station.isconnected():
        pass

    station.ifconfig()

    state['station'] = station
    
    print("Connected to wifi network {}".format(state["wifi"][0]))


def init_wifi(state):
    print("loading wifi info from wifi.txt")

    with open('wifi.txt', 'r') as h:
        lines = h.read().split('\n')  # no splitlines on esp8266 build
        wifi_info = tuple([line.strip() for line in lines])

        state["wifi"] = (wifi_info[0], wifi_info[1])

    connect_wifi(state)


def tick_wifi(state):
    if state['station'] is None:
        init_wifi(state)
        return True

    elif not state['station'].isconnected():
        connect_wifi(state)
        return True
    
    return False
