import calWBGT
from SlackAPI.SlackAPI_class import SlackAPI
from sched import scheduler
import os
from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from datetime import date
import csv

def timer_loop():
    timer_sched = scheduler(time, sleep)
    current = datetime.now()
    # if current.minute < 30:
    #     current = current.replace(minute=0, second=0, microsecond=0)
    # else:
    #     current = current.replace(minute=30, second=0, microsecond=0)
    current = current.replace(microsecond=0) # for test
    next_time = current
    today = date.today()
    export_csv_name = "window-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
    if not os.path.exists(export_csv_name):
        with open(export_csv_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['date','Hum','Temp','WBGT'])

    api = SlackAPI(
        token=os.environ['SLACK_API_TOKEN'], 
        channels = '#zikkenzyou_go'
        )

    try:
        while True:
            timer_sched.enterabs(next_time.timestamp(), 1, calWBGT.calWBGT, kwargs={'csv_path': export_csv_name})
            timer_sched.run()
            # if today < date.today():
            if current + timedelta(minutes=1) < datetime.now():
                api.Visualization_HeatStroke(path=export_csv_name)
                today = date.today()
                export_csv_name = "window-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                with open(export_csv_name, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(['date','Hum','Temp','WBGT'])
                current = datetime.now().replace(microsecond=0)
            # next_time = current + timedelta(minutes=30)
            next_time = current + timedelta(seconds=5)

if __name__=='__main__':
    timer_loop()
