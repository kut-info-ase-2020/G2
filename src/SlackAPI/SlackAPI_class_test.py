import os
import slack
import numpy as np
from slack import WebClient
import requests
import matplotlib
from slack.errors import SlackApiError
import SlackAPI_class


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
Slack.Notification_Heatstroke(a,b)
Slack.Notification_Sitting(b)
Slack.Notification_Ventilation(b)

x = np.array([[1000,0],[150,1],[250 , 0],[350,1],[200,0],[50,1], [400,0]])
print(x.shape)
print(x[1,1])

Slack.Visualization_Sitting(x)
Slack.Visualization_Ventilation(x)