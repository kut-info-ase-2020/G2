from calWBGT import calWBGT
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
    cal_wbgt = calWBGT()
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

    interval = 15 #setting demo interval
    while True:
        timer_sched.enterabs(
            next_time.timestamp(), 1, run_calWBGT,
            kwargs={'today': today,
                    'current': current,
                    'csv_path': export_csv_name,
                    'interval': interval,
                    'cal_wbgt': cal_wbgt,})
        timer_sched.run()
        if today < date.today():
        #if current + timedelta(minutes=interval) < datetime.now():
            current = datetime.now()
            current = current.replace(microsecond=0) # for test
            today = date.today()
            export_csv_name = "data/heatstroke-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
            

        next_time = next_time + timedelta(minutes=15)
        # next_time = next_time + timedelta(minutes=interval)

def run_calWBGT(today, current, csv_path, interval, cal_wbgt):
    if today < date.today():
    # if current + timedelta(minutes=10) < datetime.now():
        api = SlackAPI(
            token=os.environ['SLACK_API_TOKEN'], 
            channels = '#zikkenzyou_go'
        )
        api.Visualization_HeatStroke(path=csv_path)
        csv_path = "data/heatstroke-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['date','Hum','Temp','WBGT'])
    cal_wbgt.calWBGT(csv_path)


if __name__=='__main__':
    timer_loop()
