import os

"""
This script handles the retrieval of API keys from environment variables, 
ensuring secure and convenient access to various external services. 
"""

# API key from OpenAI
OPENAIKEY = os.environ.get("OPENAIKEY")

#Telegram API
TELEGRAMKEY = os.environ.get("TELEGRAMKEY")
TELEGRAM_CHANEL_ID = os.environ.get("TELEGRAM_CHANEL_ID")

# Eleven Labs API
ELEVENLABS_KEY = os.environ.get("ELEVENLABS_API")

# Pictures
Pexels_key = os.environ.get("Pexels_key")
Unsplash_key = os.environ.get("Unsplash_key")
Pixaby_key = os.environ.get("Pixaby_key")
