from machine import Pin
from time import sleep

import dht
import tm1637


sensor = dht.DHT11(Pin(15))
tm = tm1637.TM1637(clk=Pin(16), dio=Pin(17))

state = {
    "temp": None,
    "hum": None,
}

def measure():
    global state

    sensor.measure()

    temp = sensor.temperature()
    hum = sensor.humidity()

    state = {
        "temp": temp,
        "hum": hum,
    }


def status_loop():
    tick = 0

    while True:
        if tick % 2 == 0:
            measure()

        if state["temp"] is None:
            measure()
            tm.show("-**-")
        elif tick % 2 == 0:
            tm.temperature(state["temp"])
        else:
            tm.scroll("Humidity {}".format(state["hum"]))

        tick += 1
        sleep(1)

status_loop()