import smtplib
import imaplib
import email
from backend.mail import ServerEmail
from typing import List, Tuple
class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, imapserv, port_w_tls, port) -> None:
        self.host = smtpserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv)
        
        self.imap = None
        self.imap_host = imapserv
        if(imapserv):
            self.imap = imaplib.IMAP4_SSL(imapserv)

        self._folders = []
        self._message_count = 0

    def connect(self):
        "Connect to the mail server"
        print("connecting", self.host, self.port_tls, self.port)
        self.server.connect(self.host, self.port_tls or self.port)

        # Starts the process
        self.server.ehlo()
        if self.port_tls:
            self.server.starttls()
            self.server.ehlo()

    def login(self, email, password):
        "Log into the mail server"
        self.server.login(email, password)

        if self.imap:
            self.imap.login(email, password)

    def select_folder(self, folder: str):
        print("selecting folder", folder)
        f = folder.lower()
        if not self._folders:
            self.get_folders()
        for name, _ in self._folders:
            if f == name.lower():
                break
        else:
            return

                
        status, msg = self.imap.select(f)
        if status:
            self._message_count = int(msg[0])
        else:
            self._message_count = 0
        return status

    def get_message_count(self):
        return self._message_count

    def fetch(self, limit=10, start_from=0) -> List[ServerEmail]:
        "Fetch emails"
        emails = []
        if self._message_count:
            limit = min(self._message_count, limit)
            print("limit", limit)
            # https://stackoverflow.com/questions/2177306/imap-search-limit-the-number-of-messages-returned
            res, messages = self.imap.search(None, 'ALL')
            if res:
                messages = messages[0].split()
                if start_from > self._message_count:
                    start_from = 0
                print("start from", start_from)
                for i in range(1, limit + 1):
                    num = (start_from + i)
                    res, msg = self.imap.fetch(messages[-num], "(RFC822)")
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

    def get_folders(self) -> List[Tuple]:
        if not self._folders:
            self._folders = [x for x in self.imap.list()[1]]

            self._folders = [(f.decode().split(' "/" ')[1], f) for f in self._folders]

        fs = self._folders.copy()

        # filter nonstandard folders
        for f in fs.copy():
            if 'fejl' in f[0].lower() or 'error' in f[0].lower():
                fs.remove(f)

            # move inbox to top
            if 'inbox' in f[0].lower():
                fs.remove(f)
                fs.insert(0, f)

        return fs

    def send(self, sender, reciepient, emailbody):
        "Send email through mailserver"
        self.server.sendmail(sender, reciepient, emailbody)

    def quit(self):
        "Quit the server"
        self.server.quit()

        # #temp solution
        # if (imap_gear == 1):
        #     self.imap.close()
        #     self.imap.logout()

