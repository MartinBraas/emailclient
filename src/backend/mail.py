# None essential importations for different purposes
from email import encoders, message
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from email import message_from_bytes
from typing import Match
from . import variables as v
from array import array as arr
import re

class Email:
    """
    A class to encapsulate a single email
    """

    def __init__(self) -> None:
        self.msg = MIMEMultipart()

    def setRecipient(self, sender_name, recipient_email):
        "Set the recipient of the email. Sender name is the name of the sender"
        self.msg['From'] = sender_name
        self.msg['To'] = recipient_email

    def setCC(self, cc):
        self.msg['Cc'] = cc

    def setBCC(self, bcc):
        self.msg['Bcc'] = bcc

    def setSubject(self, text):
        "Set the subjcet of the email"
        self.msg['Subject'] = text

    def setBody(self, text, type='plain'):
        "Set the body of the email"
        self.msg.attach(MIMEText(text, type))

    def addAttachment(self, name, content):
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(content)

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={name}')
        self.msg.attach(p)

    def getString(self):
        return(self.msg.as_string())

    def getMessage(self):
        return self.msg
        

class ServerEmail:  # pragma: no cover
    """
    A class to encapsulate a single email from the server
    """

    def __init__(self, mail_id, msg: message.EmailMessage) -> None: 
        self.mail_id = mail_id
        self.msg = msg
        self.from_ = ''
        self.cc = ''
        self.bcc = ''
        self.subject = ''
        self.body = ''
        self.content_disposition = ''
        self.content_type = ''

        self._parse()

    def _parse(self): # pragma: no cover
        msg = self.msg

        if msg["Subject"]:
            # decode the email subject
            self.subject, encoding = decode_header(msg["Subject"])[0]
            if not encoding:
                encoding = 'utf-8'
            if isinstance(self.subject, bytes):
                # if it's a bytes, decode to str
                self.subject = self.subject.decode(encoding)

        # decode email sender
        if msg["From"]:
            self.from_, encoding = decode_header(msg.get("From"))[0]
            if not encoding:
                encoding = 'utf-8'
                # v.reply_btn(self.from_)
            if isinstance(self.from_, bytes):
                self.from_ = self.from_.decode(encoding)
                # v.reply_btn(self.from_) 


    def get_id(self):
        return self.mail_id

    def get_recipents(self, include_name = True):
        "Get the recipient of the email"
        # v.reply_btn(self.from_)
        f = self.from_
        if not include_name:
            m: Match = re.search("<(.+)>", f)
            if m:
                f = m.group(1)
        return f

    def get_subject(self):
        "Get the subjcet of the email"
        return self.subject

    def get_body(self):
        "get the body of the email"
        if self.body:
            return self.body
        msg = self.msg
        # if the email message is multipart
        if msg.is_multipart():
            # iterate over email parts
            for part in msg.walk():
                # extract content type of email
                self.content_disposition = str(part.get("Content-Disposition"))
                if 'attachment' in self.content_disposition:
                    continue
                try:
                    # get the email body
                   m = message_from_bytes(part.get_payload(decode=True))
                   self.body = m.as_string()
                   self.content_type = part.get_content_type()
                except Exception as e:
                    print(e)
            print(self.content_type, self.content_disposition)
        else:
            # extract content type of email
            self.content_type = msg.get_content_type()
            # get the email body
            try:
                m = message_from_bytes(msg.get_payload(decode=True))
                self.body = m.as_string()
            except Exception as e:
                    print(e)

        return self.body

    def get_content_type(self):
        return self.content_type

    def get_content_disposition(self):
        return self.content_disposition
        
    def get_attachment(self):
        data = list(self.msg.iter_attachments())
        attachments = []
        for a in data:
            attachments.append((a.get_filename(), a.get_payload(decode=True)))
            
        return attachments
    
    def get_date(self):
        msg = self.msg
        date = msg["Date"]
        return date