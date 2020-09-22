import slack
import random
import os
@slack.RTMClient.run_on("pin_added")
def fortune(**payload):
    print("responce get!")
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    print(data)
    # textはreplyなどには含まれないので、subtypeがなし=親メッセージかを確認する
    if 'subtype' not in data and 'fortune' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        num = random.randint(0, 2)
        if num == 0:
            kichi = "daikichi"
        elif num == 1:
            kichi = "kichi"
        elif num == 2:
            kichi = "kyou"
        # thread_tsを設定することでスレッドでのリプライになる
        web_client.chat_postMessage(
            channel=channel_id,
            text=kichi,
            thread_ts=thread_ts
        )
slack_token = os.environ["SLACK_API_TOKEN"]
web_client = slack.WebClient(token=slack_token)
response = web_client.chat_postMessage(
    channel='zikkenzyou_go',
    text='fortune!'
)

rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()