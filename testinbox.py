# -*- coding:utf-8 -*-
###
# --------------------------------------------------------------
# Modified Date: Thursday, 11th June 2020 9:49:12 pm
# Modified By: Ritesh Singh
# --------------------------------------------------------------
###
import logging, logging.config
import sys
import imaplib
import email
from email.header import decode_header
import re
import time
from config import Config

class EmailRead:
    def decode_content(self, content):
        encodings = ['utf-8', 'ascii', 'iso-8859-1', 'windows-1252']
        for encoding in encodings:
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue
        return content.decode('utf-8', errors='replace')
    
    def read_emails(self):
        try:
            mail = imaplib.IMAP4_SSL(self.smtp_server)
            mail.login(self.email_address, self.password)
            mail.select(self.label, readonly=True)
            
            # Correct usage of uid search
            result, data = mail.uid('search', None, 'ALL')
            
            if result != 'OK':
                self.logger.error(f"Search failed: {result}")
                return []

            self.logger.info('Processing mailbox...')
            
            ids = data[0].split()
            if not ids:
                self.logger.info("No emails found in the inbox.")
                return []
            
            emails = []
            for email_id in ids[-50:]:
                result, data = mail.uid('fetch', email_id, "(RFC822)")
                if result != 'OK':
                    self.logger.error(f"Fetch failed for email {email_id}: {result}")
                    continue

                raw_email = data[0][1]  # The email body is the second part of the tuple
                email_message = email.message_from_bytes(raw_email)
                subject = email_message['Subject']
                # if subject:
                #     # Decode the subject if it's encoded
                #     decoded_subject = decode_header(subject)[0][0]
                #     if isinstance(decoded_subject, bytes):
                #         decoded_subject = decoded_subject.decode()
                #     self.subject.append(decoded_subject)

                # Extract Subject
                subject = decode_header(email_message['Subject'])[0][0]
                subject = subject.decode() if isinstance(subject, bytes) else subject

                # Extract From
                from_header = decode_header(email_message['From'])[0][0]
                from_header = from_header.decode() if isinstance(from_header, bytes) else from_header

                # Extract Body
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = self.decode_content(part.get_payload(decode=True))
                            break
                else:
                    body = self.decode_content(email_message.get_payload(decode=True))
                
                emails.append(
                    {
                        'Subject': subject,
                        'From': from_header,
                        'Content': body
                    }
                )

            return emails

        except imaplib.IMAP4.error as e:
            self.logger.error(f"IMAP error: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Error in reading your {self.label} label: {e}", exc_info=True)
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass
        
        return []


    def __init__(self, email_address=None, password=None):
        cfg = Config()
        # logging.config.fileConfig('log.ini')
        self.logger = logging.getLogger('sLogger')
        self.subject = []
        self.smtp_server = "imap.gmail.com"
        self.email_address = email_address if email_address else cfg.gmail_user
        self.password = password if password else cfg.gmail_pwd
        self.label = '"'+'Inbox'+'"'
        # self.from_date = config.from_date
        # self.to_date = config.to_date
        self.command = 'ALL'#'(SINCE "' + self.from_date + '" BEFORE "' + self.to_date + '")'
        

# if __name__ == '__main__':
#     r1 = EmailRead()
#     data = r1.read_emails()
#     print(len(data))
#     if len(data) > 0:
#         for i in data:
#             print(i)
#             time.sleep(.2)