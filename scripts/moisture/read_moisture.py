import machine

import utime as time

from controller import init_link, post_data
from esp8266_i2c_lcd import I2cLcd

adc = machine.ADC(machine.Pin(32))
adc.atten(machine.ADC.ATTN_11DB)

def read_avg(ticks=1):
    vals = []

    for _ in range(ticks):
        time.sleep_ms(200)
        vals.append(adc.read())

    return sum(vals) / ticks

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

buzzer = machine.Pin(4, machine.Pin.OUT)

def signal_sos(label):
    lcd.clear()
    lcd.putstr("Need water...")

    for i in range(3):
        buzzer.on()
        time.sleep_ms(200)
        buzzer.off()
        time.sleep_ms(300)

    lcd.clear()
    lcd.putstr(label)

    for i in range(3):
        buzzer.on()
        time.sleep_ms(400)
        buzzer.off()
        time.sleep_ms(300)

    lcd.clear()
    lcd.putstr("Need water...")

    for i in range(3):
        buzzer.on()
        time.sleep_ms(200)
        buzzer.off()
        time.sleep_ms(300)

    lcd.clear()
    lcd.putstr(label)


while True:
    buzzer.off()

    try:
        ######################
        # Sensor calibration #
        ######################

        # air = 3750 (0%)
        # water = 1450 (100%)
        # max int = 4095
        # The Difference     = 3750 - 1450 = 2300
        # 1 %                = 2300 / 100 = 23
        base = read_avg()
        fraction = min(max((3750 - base) / (3750 - 1450), 0), 1)
        value = fraction * 100

        timestamp = '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.0Z'.format(*time.localtime())
        label = "Raw: {}\nWet: {:.1f}%".format(round(base), round(value, 1))

        lcd.clear()
        lcd.putstr(label)

        if value < 60:
            signal_sos(label)

        # print("{}: raw {}, fraction {}".format(timestamp, base, fraction))
        # addr = init_link('moisture-1')
        # post_data(addr, '/api/moisture', data={'value': value, 'timestamp': timestamp})

    except Exception as e:
        print('Error')
        print(e)
        machine.reset()

    time.sleep(5)

#sleep_delay = 60 * 1000 # * 10
#machine.deepsleep(sleep_delay)
