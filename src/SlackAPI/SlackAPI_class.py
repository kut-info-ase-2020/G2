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

    def Notification_send(self,text):
        try:
            print("notification send!")
            #warningを通知
            response = self.client.chat_postMessage(
                channel=self.channels,
                text=text
            )
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]

    def Notification_WBGT(self,Temp,Hum):
        try:
            print("WBGT notification message create...")

            message = "熱中症の危険があります！窓を開ける、エアコンを起動するなどの対策を行ってください！\n室温 = "+ str(Temp) + "度\n湿度 = " + str(Hum) + "度"
            self.Notification_send(message)
        except ValueError:
            print("エラー！数字以外の文字が入力されているかも")
        
    def Visualization(self,image,sensor_type,text):
        try:
            print(sensor_type + "'s notification send!")
            
            #画像ファイルを送信
            url = "https://slack.com/api/files.upload"
            data = {
                "token": self.token,
                "channels": self.channels,
                "title": "test file",
                "initial_comment": sensor_type + "_sensor is warning!!\n" + text
              }
            requests.post(url, data=data, files=image)
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    