import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        self.openai_key = os.getenv('OPENAI_KEY')
        self.openai_api_base = os.getenv('OPENAI_API_BASE')

        # Gmail cred
        self.gmail_user = os.getenv('GMAIL_USERNAME')
        self.gmail_pwd = os.getenv('GMAIL_PASSWORD')

config = Config()