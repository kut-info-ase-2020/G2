import os
import slack
from slack import WebClient
import requests
import matplotlib
from slack.errors import SlackApiError

class SlackAPI:
    def __init__(self, token,channels):
        self.client = slack.WebClient(token)
        self.channels = channels
        self.token = token
        print("setting finish")
    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(
                channel=self.channels,
                text=message
            )
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]

    def visualization(self,image,text):
        try:
            print(text + "'s visualization send!")
            
            #画像ファイルを送信
            url = "https://slack.com/api/files.upload"
            data = {
                "token": self.token,
                "channels": self.channels,
                "title": "test file",
                "initial_comment": "warning!!\nWBGT is 35!!!\n you must die"
              }
            requests.post(url, data=data, files=image)
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]        
        

token=os.environ['SLACK_API_TOKEN']
channels = '#zikkenzyou_go'
print("class test now...")

Slack = SlackAPI(token,channels)
message = "wow!"

Slack.send_message(message)

files = {'file': open("test.png", 'rb')}
Slack.visualization(files,text = "sitting")