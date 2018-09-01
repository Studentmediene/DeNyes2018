import os

from slackclient import SlackClient


def send_message(msg):
    client = SlackClient(os.environ['SLACK_API_TOKEN'])
    return client.api_call(
      "chat.postMessage",
      channel="#de-nyes",
      text=msg
    )
