# Enable debug logging
import logging
import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)


class slack_service:
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.client = WebClient(token=self.token)
        self.slack_channel_id = os.getenv("SLACK_CHANNEL_ID")

    def send_message(self, channel: str, message: str):
        # Here you would implement the logic to send a message to Slack using the Slack API.
        # This is a placeholder implementation.
        print(f"Sending message to Slack channel {channel}: {message}")

        try:
            if not self.slack_channel_id:
                raise ValueError(
                    "SLACK_CHANNEL_ID environment variable is not set."
                )
            response = self.client.chat_postMessage(
                channel=self.slack_channel_id, text=message
            )
            assert response["ok"]
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response[
                "error"
            ]  # str like 'invalid_auth', 'channel_not_found'
