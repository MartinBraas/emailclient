import smtplib
import imaplib
import email
from mail import ServerEmail
from typing import List
class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, imapserv, port_w_tls, port) -> None:
        global imap_gear
        self.host = smtpserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv, port_w_tls, port)
        
        #temp solution
        imap_gear = 0
        if(imapserv != 0):
            self.imap = imaplib.IMAP4_SSL(imapserv)
            self.imap_host = imapserv
            self._folders = []
            imap_gear = 1

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

        #temp solution
        if(imap_gear == 1):
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

    def fetch(self, limit=10, folder="INBOX") -> List[ServerEmail]:
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

        #temp solution
        if (imap_gear == 1):
            self.imap.close()
            self.imap.logout()

