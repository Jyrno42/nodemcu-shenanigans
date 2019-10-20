import time

from machine import Pin


def blink_led(pin_id):
    led = Pin(pin_id, Pin.OUT)
    led.off()

    while True:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

# IO15 connected to input of led
# GND connected to 1K transistor -> output of led
blink_led(15)
