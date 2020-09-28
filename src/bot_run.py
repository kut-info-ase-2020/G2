import os
from slack import RTMClient
from slack.errors import SlackApiError

import sys
from SlackAPI import SlackAPI_class


from weatherAPI import weather

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
    if  'subtype' not in data and 'help' in data['text']:
        res_message =  "Here's how to set up a region for weather information.\nThis service allows you to set up your own region by typing a command.\n\n[set-Placename,{place-name}]\nSet by region name\n{place-name} is Enter a place name like tokyo,kochi\nfor example:Set-Placename,kochi\n\n[set-location,{latitude},{longitude}]\nSet by latitude and longitude\n{latitude}{longitude} is input a number of latitude and longitude\nfor example:Set-Location,30,30\n\n[Change-Mode,{mode-name}]\nChange mode,placemode or location\nPlaceName mode:[Change-mode,PlaceName]\nLocation mode:[Change-mode,Location]\n\n[Check-Mode]:Check Current Mode type"
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

    elif  'subtype' not in data and 'Set-Placename,' in data['text']:
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

    elif  'subtype' not in data and 'Set-Location,' in data['text']:
        s = message.split(',')
        print(s)
        ido = s[1]
        keido = s[2]
        print(ido)
        print(keido)
        weather_result_message = weatherAPI.set_location(int(ido),int(keido))
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
    elif  'subtype' not in data and 'Change-Mode,' in data['text']:
        s = message.split(',')
        print(s)
        mode = s[1]
        #keido = s[2]
        print(mode)
        weather_result_message = weatherAPI.change_mode(mode)
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
    elif  'subtype' not in data and 'Check-Mode' in data['text']:
        #s = message.split(',')
        #print(s)
        #mode = s[1]
        #keido = s[2]
        #print(mode)
        mode = weatherAPI.mode
        print(mode)
        #weather_result_message = weatherAPI.mode
        if mode == 0:
        	weather_result_message="Current Mode is PlaceName Mode!"
        else:
        	weather_result_message="Current Mode is Location Mode!"
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
    elif 'B0190A265JA' not in data['bot_id']:
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

message = "Hello.Here you can set up your region to be used in the ventilation notification system.\n[help] is Check the tutorial."
Slack.send_message(message)

message = 'kochi'
weatherAPI = weather.Weather()
weather_result_message = weatherAPI.set_placename(message)
print(weather_result_message)

tokenkey = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token = tokenkey)
print("Hello_test")
rtm_client.start()
