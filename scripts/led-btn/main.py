from machine import Pin
from time import sleep

led = Pin(16, Pin.OUT)
button = Pin(15, Pin.IN)

def on_when_pressed():
    while True:
        led.value(button.value())
        sleep(0.1)

def on_off_state():
    is_on = False

    prev_btn_val = button.value()

    while True:
        led.value(0 if is_on else 1)

        btn_val = button.value()

        if prev_btn_val == 1 and btn_val == 0:
            is_on = not is_on
        
        prev_btn_val = btn_val
        
        sleep(0.1)

on_off_state()
