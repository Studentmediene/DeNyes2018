import os

from slackclient import SlackClient


client = SlackClient(os.environ['SLACK_API_TOKEN'])
