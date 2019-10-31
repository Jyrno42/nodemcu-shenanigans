import machine


adc = machine.ADC(machine.Pin(32))
adc.atten(machine.ADC.ATTN_11DB)


try:
    ######################
    # Sensor calibration #
    ######################

    # values on right are inverse * 1000 values on left
    # dry air = 3750 (0%)
    # water = 1450 (100%)
    # The Difference     = 3750 - 1450 = 2300
    # 1 %                = 2300 / 100 = 23

    hours = str(time.localtime()[3])
    mins = str(time.localtime()[4])
    secs = str(time.localtime()[5])

    if int(secs) < 10:
        secs = '0' + secs
    if int(mins) < 10:
        mins = '0' + mins
    timestr = hours + ':' + mins + ':' + secs

    fraction = min(max((3750 - adc.read()) / (3750 - 1450), 0), 1)
    SoilMoistVal = fraction * 100

    print('fr', fraction, 'val', SoilMoistVal)

except:
    machine.reset()
