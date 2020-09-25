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
    export_csv_name = "data/heatstroke-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
    if not os.path.exists(export_csv_name):
        with open(export_csv_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['date','Hum','Temp','WBGT'])

    api = SlackAPI(
        token=os.environ['SLACK_API_TOKEN'], 
        channels = '#zikkenzyou_go'
        )

    while True:
        timer_sched.enterabs(next_time.timestamp(), 1, calWBGT.calWBGT, kwargs={'csv_path': export_csv_name})

        if today < date.today():
        # if current + timedelta(minutes=30) < datetime.now():
            api.Visualization_HeatStroke(path=export_csv_name)
            today = date.today()
            export_csv_name = "data/heatstroke-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
            with open(export_csv_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['date','Hum','Temp','WBGT'])
            current = datetime.now()
            current = current.replace(microsecond=0) # for test
        
        timer_sched.run()
        current = next_time
        next_time = next_time + timedelta(minutes=10)
        # next_time = next_time + timedelta(minutes=1)

if __name__=='__main__':
    timer_loop()
