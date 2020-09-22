# from ventilation_sensor.reedswitch import ReedSwitch
from ventilation_sensor.stubs.dummysensor import ReedSwitch
from sched import scheduler
from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
from collections import namedtuple

class WindowOpeningTimer:
    """WindowOpeningTimer
    起動すると，30分に1度，1秒間隔で1分間リードスイッチの値を読み取る
    そのたびにwindow-Y-M-D.csvに保存していく
    起動時に12時を超えてしまった場合のためにタイマー設定後に確認が必要かも？
    """
    def no_use_func(a = None, b = None, c = None):
        pass
    window_open_timer_func = no_use_func
    window_opened_func = no_use_func
    periodical_report_func = no_use_func
    WindowStatus = namedtuple('WindowStatus', ['opening', 'closing'])
    window_status = WindowStatus(opening=0, closing=1) # 暫定
    window_status_now = window_status.closing
    WindowData = namedtuple('WindowData', ['time', 'flag'])
    closed_time = 0
    DATA_PATH = "./data/"

    def start(self):
        self.reed_switch = ReedSwitch(port=26)
        self.timer_loop()

    def timer_loop(self):
        timer_sched = scheduler(time, sleep)
        current = datetime.now()
        # if current.minute < 30:
        #     current = current.replace(minute=0, second=0, microsecond=0)
        # else:
        #     current = current.replace(minute=30, second=0, microsecond=0)
        current = current.replace(microsecond=0) # for test
        next_time = current
        today = date.today()
        next_csv_name = "window-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
        if not os.path.exists(WindowOpeningTimer.DATA_PATH + next_csv_name):
            self.write_csv(next_csv_name, WindowOpeningTimer.WindowData(time=current.replace(hour=0, minute=0).strftime("%H%M"), flag=WindowOpeningTimer.window_status_now))
        try:
            while True:
                timer_sched.enterabs(next_time.timestamp(), 1, self.measurement_next)
                timer_sched.run()
                if today < date.today():
                # if current + timedelta(minutes=1) < datetime.now():
                    export_csv_name = WindowOpeningTimer.DATA_PATH + "window-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                    self.periodical_report_func(export_csv_name)
                    today = date.today()
                    current = datetime.now().replace(microsecond=0)
                    next_csv_name = "window-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                    if not os.path.exists(WindowOpeningTimer.DATA_PATH + next_csv_name):
                        self.write_csv(next_csv_name, WindowOpeningTimer.WindowData(time=current.replace(hour=0, minute=0).strftime("%H%M"), flag=WindowOpeningTimer.window_status_now))
                # next_time = next_time + timedelta(minutes=30)
                # next_time = next_time + timedelta(minutes=1)
                next_time = next_time + timedelta(seconds=30)
        except KeyboardInterrupt:
            self.destroy()

    def measurement_next(self):
        (date, result) = self.get_window_status()
        csv_name = "window-" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".csv"
        if result.flag == WindowOpeningTimer.window_status.closing:
            self.closed_time += 30
            if self.closed_time > self.window_open_timer_interval:
                self.window_open_timer_func(int(self.closed_time/60), self.closed_time%60)
        if self.window_status_now != result.flag:
            self.write_csv(csv_name, result)
            if result.flag == WindowOpeningTimer.window_status.opening:
                self.window_opened_func()
                self.closed_time = 0
            self.window_status_now = result.flag

    def write_csv(self, filename, data):
        if not os.path.exists(WindowOpeningTimer.DATA_PATH):
            os.mkdir(WindowOpeningTimer.DATA_PATH)
        filepath = WindowOpeningTimer.DATA_PATH + filename
        # if not os.path.exists(filepath):
        with open(filepath, mode='a') as f:
                # f.write("time,flag\n")
            f.write(str(data.time) + "," + str(data.flag) + "\n")
        # else:
        #     with open(filepath, mode='w') as f:
        #         f.write(str(data.time) + "," + str(data.flag) + "\n")

    def get_window_status(self):
        msr_sched = scheduler(time, sleep)
        start_time = datetime.now().replace(microsecond=0)
        next_time = start_time + timedelta(seconds=1)
        # end_time = start_time + timedelta(minutes=1)
        end_time = start_time + timedelta(seconds=5)
        read_values = []
        while next_time < end_time:
            msr_sched.enterabs(next_time.timestamp(), 1, self.read_next, argument=(self.reed_switch, read_values))
            msr_sched.run()
            next_time = next_time + timedelta(seconds=1)
        average = int(0.5 + sum(read_values)/len(read_values))
        time_str = start_time.strftime("%H%M")
        status = None
        if average == WindowOpeningTimer.window_status.closing:
            status = WindowOpeningTimer.window_status.closing
        else:
            status = WindowOpeningTimer.window_status.opening
        return (start_time, WindowOpeningTimer.WindowData(time=time_str, flag=status))

    def read_next(self, sensor, res_list):
        res_list.append(sensor.read())

    def set_time_over_callback(self, *, interval=120, func):
        # 窓が開いたままinterval min.過ぎるとfuncを呼び出す
        self.window_open_timer_interval = interval
        self.window_open_timer_func = func

    def set_window_open_callback(self, *, func):
        # 窓が開くとfuncを呼び出す
        self.window_opened_func = func

    def set_period_callback(self, *, func):
        # 定時報告
        self.periodical_report_func = func

    def call_time_over_callback(self, hour, minute):
        self.window_open_timer_func(hour, minute)

    def call_window_open_callback(self):
        self.window_opened_func()

    def call_period_callback(self, path):
        self.periodical_report_func(path)

    def destroy(self):
        self.window_open_timer_func = WindowOpeningTimer.no_use_func
        self.window_open_timer_interval = 0
        self.window_opened_func = WindowOpeningTimer.no_use_func
        self.periodical_report_func = WindowOpeningTimer.no_use_func
        self.window_status_now = WindowOpeningTimer.window_status.closing
        self.reed_switch.destroy()
