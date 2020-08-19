import os
import slack
import numpy as np
import pandas as pd
from slack import WebClient
import requests
import matplotlib
from slack.errors import SlackApiError
import SlackAPI_class
import io


token=os.environ['SLACK_API_TOKEN']
channels = '#zikkenzyou_go'
print("class test now...")

Slack = SlackAPI_class.SlackAPI(token,channels)

message = "wow!"
Slack.send_message(message)

files = {'file': open("test.png", 'rb')}
sensor_type = "PIR"
text = "you must stand up!"
a = 1
b = 2
Slack.Notification_HeatStroke(a,b)
Slack.Notification_Sitting(b)
Slack.Notification_Ventilation(b)

x = np.array([[1000,0],[150,1],[250 , 0],[350,1],[200,0],[50,1], [400,0]])
#x = np.array([[10:10:00,0],[13:13:00,1],[15:15:00 , 0],[16:16:00,1]])
print(x)
path = 'Sitting.csv'
np.savetxt(path,x,fmt='%d')
print(np.loadtxt(path,dtype='int64'))

Slack.Visualization_Sitting(path)
Slack.Visualization_Ventilation(path)

data = """date,Hum,Temp,WBGT
2018-11-01 00:00:00,65,28,14
2018-11-01 01:01:00,26,28,15
2018-11-01 02:02:00,47,26,17
2018-11-01 03:03:00,20,25,18
2018-11-01 04:04:00,65,26,19
2018-11-01 05:05:00,24,25,14
2018-11-01 06:06:00,31,23,15
2018-11-01 07:07:00,21,27,14
2018-11-01 08:08:00,98,28,27
2018-11-01 09:09:00,48,28,22
2018-11-01 10:10:00,18,29,24
2018-11-01 11:11:00,86,31,31
2018-11-01 12:12:00,21,33,27
2018-11-01 13:13:00,98,32,31
2018-11-01 14:14:00,48,33,30
2018-11-01 15:15:00,18,34,26
2018-11-01 16:16:00,21,30,25
2018-11-01 17:17:00,98,27,25
2018-11-01 18:18:00,48,25,22
2018-11-01 19:19:00,18,22,19
2018-11-01 20:20:00,21,20,18
2018-11-01 21:21:00,98,18,19
2018-11-01 22:22:00,48,16,14
2018-11-01 23:23:00,18,11,9"""
df = pd.read_csv(io.StringIO(data), parse_dates=[0])
path = 'HeatStroke.csv'
df.to_csv(path)

Slack.Visualization_HeatStroke(path)



