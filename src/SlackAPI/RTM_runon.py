import os
from slack import RTMClient
from slack.errors import SlackApiError


@RTMClient.run_on(event="message")
async def say_hello(**payload):
    """"Hello" を含んだメッセージに反応して "Hi @<user名>" を返す """
    data = payload["data"]
    web_client = payload["web_client"]

    if "text" in data and "Hello" in data.get("text", []):
        channel_id = data["channel"]
        thread_ts = data["ts"]
        user = data["user"]

        await web_client.chat_postMessage(
            channel=channel_id, text=f"Hi <@{user}>!", thread_ts=thread_ts
        )


if __name__ == "__main__":
    import asyncio

    rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"], run_async=True)
    print("asyncio")
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(rtm_client.start())