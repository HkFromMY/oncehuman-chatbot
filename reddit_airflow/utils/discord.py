from .constants import DISCORD_WEBHOOK

import requests

def send_discord_message(message):
    """
        Post message to discord webhook for notification
    """
    try:
        requests.post(DISCORD_WEBHOOK, data={"content": message})

    except Exception as e:
        raise Exception(f"Error posting message to Discord: \n {repr(e)}")