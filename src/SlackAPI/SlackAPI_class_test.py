import os
import slack
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
Slack.Notification_WBGT(a,b)