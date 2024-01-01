import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = urllib.parse.quote(os.getenv("TELEGRAM_API_KEY").encode("UTF-8"))
