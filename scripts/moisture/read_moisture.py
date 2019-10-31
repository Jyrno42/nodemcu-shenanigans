import machine

import utime as time

from controller import init_link, post_data

adc = machine.ADC(machine.Pin(32))
adc.atten(machine.ADC.ATTN_11DB)

def read_avg(ticks=3):
    vals = []

    for _ in range(ticks):
        time.sleep_ms(100)
        vals.append(adc.read())

    print (vals)

    return sum(vals) / ticks

try:
    ######################
    # Sensor calibration #
    ######################

    # air = 3750 (0%)
    # water = 1450 (100%)
    # The Difference     = 3750 - 1450 = 2300
    # 1 %                = 2300 / 100 = 23
    base = read_avg()
    fraction = min(max((3750 - base) / (3750 - 1450), 0), 1)
    value = fraction * 100

    timestamp = '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.0Z'.format(*time.localtime())

    addr = init_link('moisture-1')
    post_data(addr, '/api/moisture', data={'value': value, 'timestamp': timestamp})

except Exception as e:
    print('Error')
    print(e)
    machine.reset()

sleep_delay = 60 * 1000 # * 10
machine.deepsleep(sleep_delay)
