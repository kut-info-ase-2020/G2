import os
from slack import RTMClient
from slack.errors import SlackApiError

import sys
sys.path.append('../')
import SlackAPI_class

@RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    print(data)
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    #if 'text' in data and 'Hello' in data.get('text', []):
    message = data.get('text')
    print(message)
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    try:
        response = web_client.chat_postMessage(
            channel=channel_id,
            text="地域情報を設定しました！",
            thread_ts=thread_ts
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


token=os.environ['SLACK_API_TOKEN']
channels = '#zikkenzyou_go'
print("class test now...")

Slack = SlackAPI_class.SlackAPI(token,channels)

message = "wow!"
Slack.send_message(message)

tokenkey = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token = tokenkey)
print("Hello_test")
rtm_client.start()
