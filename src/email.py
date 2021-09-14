# None essential importations for different purposes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


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
        self.msg.as_string()
