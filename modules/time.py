import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class Time:
    def get_time(self, input_text=""):
        current_time = datetime.now().strftime("%H:%M")
        return f"It's {current_time} {os.getenv('USER_TITLE')}."