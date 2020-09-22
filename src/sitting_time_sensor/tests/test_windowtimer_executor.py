from sys import argv
from sys import exit
from sys import stderr
from windowtimer import WindowOpeningTimer
from datetime import datetime
from stubs.dummysensor import ReedSwitch
import os

def tov_func(hour, minute):
    print(str(hour) + ":" + str(minute))

def prd_func(path):
    print(path)

def wop_func():
    print("opened")

if (len(argv) < 2):
    print("invalid input")
    exit(1)
timer = WindowOpeningTimer()
if argv[1] == 'run':
    timer.set_window_open_callback(func=wop_func)
    timer.set_time_over_callback(interval=40, func=tov_func)
    timer.set_period_callback(func=prd_func)
    timer.start()
elif argv[1] == 'wst':
    timer.reed_switch = ReedSwitch(port=26)
    ReedSwitch.read_value = int(argv[2])
    (date, result) = timer.get_window_status()
    print(result, file=stderr)
    print(result.flag)
elif argv[1] == 'msr_nxt':
    timer.reed_switch = ReedSwitch(port=26)
    timer.set_time_over_callback(interval=int(argv[2]), func=tov_func)
    timer.set_window_open_callback(func=wop_func)
    timer.measurement_next()
    ReedSwitch.read_value = 1
    timer.measurement_next()
elif argv[1] == 'write_csv':
    timer.write_csv("test.csv", WindowOpeningTimer.WindowData(time=argv[2], flag=int(argv[3])))
    path = WindowOpeningTimer.DATA_PATH + "test.csv"
    with open(path, mode='r') as f:
        s = f.read()
        print(s)
    os.remove(path)
elif argv[1] == 'read_next':
    tl = []
    sensor = ReedSwitch(port=0)
    ReedSwitch.read_value = int(argv[2])
    timer.read_next(sensor, tl)
    print(tl)
elif argv[1] == 'tovclbk':
    timer.set_time_over_callback(func=tov_func)
    timer.call_time_over_callback(20, 10)
    print(str(20) + ":" + str(10))
elif argv[1] == 'prdclbk':
    timer.set_period_callback(func=prd_func)
    timer.call_period_callback("/test/path")
    print("/test/path")
elif argv[1] == 'wopclbk':
    timer.set_window_open_callback(func=wop_func)
    timer.call_window_open_callback()
