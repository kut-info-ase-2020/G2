import os
import slack
from pprint import pprint

@slack.RTMClient.run_on(event="message")
def dump(**payload):
    pprint(payload)

@slack.RTMClient.run_on(event="reaction_added")
def dump2(**payload):
    pprint(payload)

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()