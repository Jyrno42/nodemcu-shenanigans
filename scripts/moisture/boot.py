import esp
import network
import machine
import gc
import time

esp.osdebug(None)

from ntptime import settime


gc.collect()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)

    with open('wifi.txt', 'r') as h:
        lines = h.read().split('\n')  # no splitlines on esp8266
        wifi_info = tuple([line.strip() for line in lines])

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_info[0], wifi_info[1])

        while not sta_if.isconnected():
            pass

try:
	do_connect()
	settime()
	
except:
	time.sleep(60)
	machine.reset()