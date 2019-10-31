import machine


# Note: Wire D0 to RST on esp8266
def deep_sleep(msecs):
    #configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
    rtc.alarm(rtc.ALARM0, msecs)

    #put the device to sleep
    machine.deepsleep()
