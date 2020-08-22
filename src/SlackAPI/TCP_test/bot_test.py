import os
from slack import RTMClient
from slack.errors import SlackApiError

import sys
sys.path.append('../')
import SlackAPI_class

sys.path.append('../../../weatherAPI/')
import weather

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
    print(user)
    if 'subtype' not in data and 'help' in data['text']:
        res_message = "helpメッセージを表示します！\n[set-location,{place-name}]と入力してください！\n{place-name}は[kochi][kami]のように半角英字で地名を入力すると地域情報を設定できます！\n地域設定が成功した場合はリプライでメッセージを送信します！\n例:set-location,kochi"
        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                text=res_message
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

    elif  'subtype' not in data and 'set-location,' in data['text']:
        s = message.split(',')
        print(s)
        place = s[1]
        print(place)
        weather_result_message = weatherAPI.set_placename(place)
        print(weather_result_message)
        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                #text="地域情報を設定しました！",
                text=weather_result_message,
                thread_ts=thread_ts
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
    else:
        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                #text="地域情報を設定しました！",
                text="type error!! \nYou should watch command[help]",
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

message = 'kochi'
weatherAPI = weather.Weather()
weather_result_message = weatherAPI.set_placename(message)
print(weather_result_message)

tokenkey = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token = tokenkey)
print("Hello_test")
rtm_client.start()
