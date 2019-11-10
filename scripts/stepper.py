import machine
import utime


class Stepper:
    def __init__(self, pin1=16, pin2=4, pin3=2, pin4=17):
        self.p1 = machine.Pin(pin1, machine.Pin.OUT)
        self.p2 = machine.Pin(pin2, machine.Pin.OUT)
        self.p3 = machine.Pin(pin3, machine.Pin.OUT)
        self.p4 = machine.Pin(pin4, machine.Pin.OUT)

        self.cfg = {
            0: {
                "p1": False,
                "p2": False,
                "p3": False,
                "p4": True,
            },
            1: {
                "p1": False,
                "p2": False,
                "p3": True,
                "p4": True,
            },
            2: {
                "p1": False,
                "p2": False,
                "p3": True,
                "p4": False,
            },
            3: {
                "p1": False,
                "p2": True,
                "p3": True,
                "p4": False,
            },
            4: {
                "p1": False,
                "p2": True,
                "p3": False,
                "p4": False,
            },
            5: {
                "p1": True,
                "p2": True,
                "p3": False,
                "p4": False,
            },
            6: {
                "p1": True,
                "p2": False,
                "p3": False,
                "p4": False,
            },
            7: {
                "p1": True,
                "p2": False,
                "p3": False,
                "p4": True,
            },
            8: {
                "p1": False,
                "p2": False,
                "p3": False,
                "p4": False,
            }
        }
    
    def tick(self, n):
        for key in sorted(self.cfg[n].keys()):
            value = self.cfg[n][key]

            p = self.__dict__[key]
        
            # print('TICK {} {} {}'.format(n, key, 'ON' if value else 'OFF'))

            if value:
                p.on()
            else:
                p.off()

    def loop(self, base_t=1000, clockwise=True, limit=400):
        n = 0

        t = base_t
        cicle = 0

        while True:
            self.tick(n)
            
            if clockwise:
                n += 1
            else:
                n -= 1

            if n > 8:
                n = 0
                cicle += 1
            elif n < 0:
                n = 8
                cicle += 1

            if cicle > 10 and cicle % 10 == 0:
                if t > 4:
                    t = int(round(t * 0.9, 0))

                    if t < limit:
                        t = limit
            
            if cicle > 10000:
                cicle = 0

            if t > 0:
                utime.sleep_us(t)
