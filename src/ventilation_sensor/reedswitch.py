import time
from collections import namedtuple
from sensor import Sensor
import RPi.GPIO as GPIO

class ReedSwitch(Sensor):
    MFStatus = namedtuple('MFStatus', ['strong', 'weak'])
    mfstatus = MFStatus(strong=0, weak=1) # 暫定
    switch_port = -1

    def setup(self, port):
        super().setup(ports=[port], port_settings=[super().INPUT])
        ReedSwitch.switch_port = port

    def read(self):
        read_val = super().read(ReedSwitch.switch_port)
        if (read_val == ReedSwitch.mfstatus.strong):
            return 1
        return 0

    def main(self):
        while True:
            time.sleep(1)
            #when motion detected turn on LED
            input = self.read()
            print("reed switch input:", input)
            if input == 1:
                print("strong magnetic force")
            else:
                print("weak magnetic force")

    def destroy(self):
        GPIO.cleanup()

    def __init__(self, port):
        self.setup(port)

if __name__ == '__main__':
    reed_switch = ReedSwitch(port=26)
    try:
        reed_switch.main()
    except KeyboardInterrupt:
        reed_switch.destroy() 
