import smtplib
import imaplib
import email
from mail import ServerEmail
class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, imapserv, port_w_tls, port) -> None:
        self.host = smtpserv
        self.imap_host = imapserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv, port_w_tls, port)
        self.imap = imaplib.IMAP4_SSL(imapserv)
        self._folders = []

    def connect(self):
        "Connect to the mail server"
        self.server.connect(self.host, self.port_tls)

        # Starts the process
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

    def login(self, email, password):
        "Log into the mail server"
        self.server.login(email, password)
        self.imap.login(email, password)

    def _select_folder(self, folder: str):
        f = folder.lower()
        if not self._folders:
            self.get_folders()
        for x in self._folders:
            if f in str(x).lower():
                f = x
                break
                
        return self.imap.select(f)

    def fetch(self, limit=10, folder="INBOX"):
        "Fetch emails"
        status, message_count = self._select_folder(folder)
        limit = min(int(message_count[0]), limit)
        res, messages = self.imap.search(None, 'UNSEEN')
        emails = []
        if res:
            messages = messages[0].split()
            for i in range(limit):
                res, msg = self.imap.fetch(messages[i], "(RFC822)")
                m = self._create_email(msg)
                if m:
                    emails.append(m)

        return emails

    def _create_email(self, msg):
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                return ServerEmail(msg)

    def get_folders(self):
        self._folders = [str(x) for x in self.imap.list()[0]]
        return self._folders

    def send(self, sender, reciepient, emailbody):
        "Send email through mailserver"
        self.server.sendmail(sender, reciepient, emailbody)

    def quit(self):
        "Quit the server"
        self.server.quit()
        self.imap.close()
        self.imap.logout()

