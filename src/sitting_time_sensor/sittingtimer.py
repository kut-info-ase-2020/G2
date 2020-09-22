from sitting_time_sensor.pir_sensor import PIRSensor
# from sitting_time_sensor.stubs.dummysensor import PIRSensor
from sched import scheduler
from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
from collections import namedtuple

class SittingTimer:
    """SittingTimer
    起動すると，30分に1度，1秒間隔で1分間PIRセンサーの値を読み取る
    そのたびにsitting-Y-M-D.csvに保存していく
    起動時に12時を超えてしまった場合のためにタイマー設定後に確認が必要かも？
    """
    def no_use_func(a = None, b = None, c = None):
        pass
    sitting_timer_func = no_use_func
    stand_func = no_use_func
    periodical_report_func = no_use_func
    SittingStatus = namedtuple('SittingStatus', ['standing', 'sitting'])
    sitting_status = SittingStatus(standing=1, sitting=0) # 暫定
    sitting_status_now = sitting_status.sitting
    SittingData = namedtuple('SittingData', ['time', 'flag'])
    sitting_time = 0
    DATA_PATH = "./data/"

    def start(self):
        self.pir_sensor = PIRSensor(port=16)
        self.timer_loop()

    def timer_loop(self):
        timer_sched = scheduler(time, sleep)
        start_time = datetime.now()
        # if current.minute < 30:
        #     current = current.replace(minute=0, second=0, microsecond=0)
        # else:
        #     current = current.replace(minute=30, second=0, microsecond=0)
        start_time = start_time.replace(second=0, microsecond=0) # for test
        next_time = start_time
        current_time = start_time
        today = date.today()
        next_csv_name = "sitting-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
        if not os.path.exists(SittingTimer.DATA_PATH + next_csv_name):
            self.write_csv(next_csv_name, SittingTimer.SittingData(time=start_time.replace(hour=0, minute=0).strftime("%H%M"), flag=SittingTimer.sitting_status_now))
        try:
            while True:
                timer_sched.enterabs(next_time.timestamp(), 1, self.measurement_next, argument=(current_time,))
                timer_sched.run()
                # if today < date.today():
                if start_time + timedelta(minutes=15) < datetime.now():
                    export_csv_name = SittingTimer.DATA_PATH + "sitting-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                    self.periodical_report_func(export_csv_name)
                    today = date.today()
                    start_time = datetime.now().replace(microsecond=0)
                    next_csv_name = "sitting-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                    if not os.path.exists(SittingTimer.DATA_PATH + next_csv_name):
                        self.write_csv(next_csv_name, SittingTimer.SittingData(time=start_time.replace(hour=0, minute=0).strftime("%H%M"), flag=SittingTimer.sitting_status_now))
                # next_time = next_time + timedelta(minutes=30)
                next_time = next_time + timedelta(minutes=1)
        except KeyboardInterrupt:
            self.destroy()

    def measurement_next(self, previous_time):
        (date, result) = self.get_window_status()
        csv_name = "sitting-" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".csv"
        if result.flag == SittingTimer.sitting_status.sitting:
            current_time = datetime.now().replace(second=0, microsecond=0)
            time_difference = current_time - previous_time
            self.sitting_time += time_difference.seconds / 60
            if self.sitting_time > self.sitting_timer_interval:
                self.sitting_timer_func(int(self.sitting_time/60), self.sitting_time%60)
        if self.sitting_status_now != result.flag:
            self.write_csv(csv_name, result)
            if result.flag == SittingTimer.sitting_status.standing:
                self.stand_func()
                self.sitting_time = 0
            self.sitting_status_now = result.flag

    def write_csv(self, filename, data):
        if not os.path.exists(SittingTimer.DATA_PATH):
            os.mkdir(SittingTimer.DATA_PATH)
        filepath = SittingTimer.DATA_PATH + filename
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
            msr_sched.enterabs(next_time.timestamp(), 1, self.read_next, argument=(self.pir_sensor, read_values))
            msr_sched.run()
            next_time = next_time + timedelta(seconds=1)
        average = int(0.5 + sum(read_values)/len(read_values))
        time_str = start_time.strftime("%H%M")
        status = None
        if average == PIRSensor.status.changed:
            status = SittingTimer.sitting_status.sitting
        else:
            status = SittingTimer.sitting_status.standing
        return (start_time, SittingTimer.SittingData(time=time_str, flag=status))

    def read_next(self, sensor, res_list):
        res_list.append(sensor.read())

    def set_time_over_callback(self, *, interval=120, func):
        # 座ったままinterval min.過ぎるとfuncを呼び出す
        self.sitting_timer_interval = interval
        self.sitting_timer_func = func

    def set_stand_callback(self, *, func):
        # 立ち上がるとfuncを呼び出す
        self.stand_func = func

    def set_period_callback(self, *, func):
        # 定時報告
        self.periodical_report_func = func

    def call_time_over_callback(self, hour, minute):
        self.sitting_timer_func(hour, minute)

    def call_stand_callback(self):
        self.stand_func()

    def call_period_callback(self, path):
        self.periodical_report_func(path)

    def destroy(self):
        self.sitting_timer_func = SittingTimer.no_use_func
        self.sitting_timer_interval = 0
        self.stand_func = SittingTimer.no_use_func
        self.periodical_report_func = SittingTimer.no_use_func
        self.sitting_status_now = SittingTimer.sitting_status.sitting
        self.pir_sensor.destroy()
