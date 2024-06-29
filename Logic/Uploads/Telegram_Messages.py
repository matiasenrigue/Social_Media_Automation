from Logic.Tools import params
import os
import asyncio
import telegram
import time
from datetime import datetime
import random

"""
This script is designed to send messages and images to a Telegram channel using the python-telegram-bot library.

It includes functions to:

    - send text messages (send_telegram)
        Utility: to inform me of issues to address regarding influencer management:
            - Scheduled videos about to run out for influencer X
            - Influencer X needs to complete the authentication workflow
            - Influencer X is running out of videos, more production is needed
        This saves me from having to be vigilant about issues, and simply be alerted to them.
"""

def send_telegram(Message: str) -> None:
    """
    Function used to send messages to Telegram.

    Parameters:
    Message (str): The content of the message to send.
    """

    async def send():
        bot = telegram.Bot(token=params.TELEGRAMKEY)
        channel_id = params.TELEGRAM_CHANEL_ID 

        while True:
            try:
                await bot.send_message(channel_id, Message)
                print("\nMessage successfully sent to Telegram.")
                break

            except Exception as e:
                print(f"\❌ Failed to send message via Telegram with error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    asyncio.run(send())
