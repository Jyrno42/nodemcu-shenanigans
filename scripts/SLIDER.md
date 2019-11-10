>>> import machine
>>> pin = machine.Pin(12)
>>> pwm = machine.PWM(pin, freq=50)
>>> pwm.duty(24)
>>> pwm.duty(126)

----

