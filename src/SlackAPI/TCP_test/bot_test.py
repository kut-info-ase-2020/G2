import os
from slack import RTMClient

# @RTMClient.run_on(event="message")
# def say_hello(**payload):
#   data = payload['data']
#   print("received", data)
#   web_client = payload['web_client']
# 
#   if 'Hello' in data['text']:
#     channel_id = data['channel']
#     thread_ts = data['ts']
#     user = data['user'] # This is not username but user ID (the format is either U*** or W***)
# 
#     web_client.chat_postMessage(
#       channel=channel_id,
#       text=f"Hi <@{user}>!",
#       thread_ts=thread_ts
#     )
@RTMClient.run_on(event="pin_added")
def print_pin(**payload):
  data = payload['data']
  print("received:", data)
  print("text:", data['item']['message']['text'])
  # web_client = payload['web_client']

  # if 'Hello' in data['text']:
  #   channel_id = data['channel']
  #   thread_ts = data['ts']
  #   user = data['user'] # This is not username but user ID (the format is either U*** or W***)

    # web_client.chat_postMessage(
    #   channel=channel_id,
    #   text=f"Hi <@{user}>!",
    #   thread_ts=thread_ts
    # )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
