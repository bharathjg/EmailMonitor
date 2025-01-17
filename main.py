from config import Config
from agents import Screener, Summarizer
# from read_inbox import read_gmail_inbox
from testinbox import EmailRead
from utils import clean_email_text
import json
import ast

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
    print(f'Processing email: {emails[:5]}')
    print('Screening...')
    screener_output = json.loads(screener.screen_emails(emails[:5]))
    print('Printing screener o/p')
    print(screener_output)

    processed_emails = process_screened_emails(screener_output, emails[:5])
    print('Printing processed screener o/p')
    print(processed_emails)

    print('Creating summarizer agent')
    summarizer = Summarizer(openai_key, base_url)
    print('Summarizing screened emails')
    summarizer_output = ast.literal_eval(summarizer.summarize_emails(processed_emails))
    print('Printing summarizer output')
    print(summarizer_output)

def process_screened_emails(screener_output, emails):
    processed_output = []
    for i in range(len(emails)):
        imp = screener_output[i]['Important']
        if imp=='Y':
            emails[i]['Important'] = imp
            processed_output.append(emails[i])
    return processed_output

def clean_emails(emails):
    for i, email in enumerate(emails):
        email['Content'] = clean_email_text(email['Content'])
        emails[i] = email
    return emails

main()