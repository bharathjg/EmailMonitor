from config import Config
from agents import Screener, Summarizer
# from read_inbox import read_gmail_inbox
from testinbox import EmailRead
from utils import clean_email_text

def main():
    cfg = Config()
    openai_key = cfg.openai_key
    base_url = cfg.openai_api_base
    username = cfg.gmail_user
    pwd = cfg.gmail_pwd
    email_reader = EmailRead(username, pwd)
    emails = email_reader.read_emails()
    emails = clean_emails(emails)

    screener = Screener(openai_key, base_url)
    print(f'Processing email: {emails[:1]}')
    print('Screening...')
    screener_output = screener.screen_emails(emails[:1])
    print('Printing screener o/p')
    print(screener_output)

    # processed_emails = process_screened_emails(screener_output)

    print('Creating summarizer agent')
    summarizer = Summarizer(openai_key, base_url)
    print('Summarizing screened emails')
    summarizer_output = summarizer.summarize_emails(screener_output)
    print('Printing summarizer output')
    print(summarizer_output)

def process_screened_emails(screener_output):
    print(screener_output)
    return

def clean_emails(emails):
    for i, email in enumerate(emails):
        email['Content'] = clean_email_text(email['Content'])
        emails[i] = email
    return emails

main()