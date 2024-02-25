import os

from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()


def send_message(text, channel='C06K2N55PQQ'):
    client = WebClient(os.environ['SLACK_BOT_KEY'])
    client.chat_postMessage(text=text, channel=channel)