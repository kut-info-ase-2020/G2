import os
import slack
from slack import WebClient
import requests
import matplotlib

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
channels = '#zikkenzyou_go'
#client = WebClient(ch_token)


#client = slack.WebClient(token='')
print("testnow")
response = client.chat_postMessage(
    channel='#zikkenzyou_go',
    text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"


url = "https://slack.com/api/files.upload"
data = {
   "token": ch_token,
   "channels": channels,
   "title": "test file",
   "initial_comment": "warning!!\nWBGT is 35!!!\n you must die"
}
files = {'file': open("test.png", 'rb')}
requests.post(url, data=data, files=files)
print("upload now...")


client = slack.WebClient(token=ch_token)
response = client.conversations_list(**{'types': 'private_channel'})
print(response.data['channels'])

