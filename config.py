from dotenv import load_dotenv
import os

load_dotenv()

# environment variables

token = os.getenv('BOT_API_TOKEN')  # telegram bot token

database_name = 'booking.db'  # database file
