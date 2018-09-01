import os

from slackclient import SlackClient


token = os.environ['SLACK_API_TOKEN']


def send_message(msg):
    client = SlackClient(token)
    return client.api_call(
      "chat.postMessage",
      channel="#de-nyes",
      text=msg
    )
