# None essential importations for different purposes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import decode_header


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
        

class ServerEmail:
    """
    A class to encapsulate a single email from the server
    """

    def __init__(self, msg) -> None:
        self.msg = msg
        self._parse()

    def _parse(self):
        msg = self.msg
        # decode the email subject
        self.subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(self.subject, bytes):
            # if it's a bytes, decode to str
            self.subject = self.subject.decode(encoding)
        # decode email sender
        self.from_, encoding = decode_header(msg.get("From"))[0]
        if isinstance(self.from_, bytes):
            self.from_ = self.from_.decode(encoding)
        self.body = ''
        self.content_disposition = ''
        # if the email message is multipart
        if msg.is_multipart():
            # iterate over email parts
            for part in msg.walk():
                # extract content type of email
                self.content_type = part.get_content_type()
                self.content_disposition = str(part.get("Content-Disposition"))
                try:
                    # get the email body
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
        else:
            # extract content type of email
            self.content_type = msg.get_content_type()
            # get the email body
            try:
                self.body = msg.get_payload(decode=True).decode()
            except:
                pass

    def get_recipents(self):
        "Get the recipient of the email"
        return self.from_

    def get_subject(self):
        "Get the subjcet of the email"
        return self.subject

    def get_body(self):
        "get the body of the email"
        self.body

    def get_attachment(self):
        return 

        
