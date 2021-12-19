from email.message import EmailMessage
import smtplib
import imaplib
import email
from .mail import ServerEmail, Email
from typing import List, Tuple
class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, imapserv, port_w_tls, port) -> None:
        self.host = smtpserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv, self.port_tls or self.port)
        
        self.imap = None
        self.imap_host = imapserv
        if(imapserv):
            self.imap = imaplib.IMAP4_SSL(imapserv)

        self._folders = []
        self._message_count = 0
        self._unread_messages = set()
        self._connected = False

    def connect(self):
        "Connect to the mail server"
        print("connecting", self.host, self.port_tls, self.port)
        self.server.connect(self.host, self.port_tls or self.port)

        # Starts the process
        self.server.ehlo()
        if self.port_tls:
            self.server.starttls()
            self.server.ehlo()

        self._connected = True

    def login(self, email, password):
        "Log into the mail server"
        if self._connected:
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
        if status == 'OK':
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
            if res == 'OK':
                unread_s, unread_mess = self.imap.search(None, '(UNSEEN)')
                if unread_s == 'OK':
                    self._unread_messages = set(unread_mess[0].split())
                messages = messages[0].split()
                if start_from > self._message_count:
                    start_from = 0
                print("start from", start_from)
                for i in range(1, limit + 1):
                    num = (start_from + i)
                    mail_id = messages[-num]
                    res, msg = self.imap.fetch(messages[-num], "(BODY.PEEK[])")
                    m = self._create_email(mail_id, msg)
                    if m:
                        emails.append(m)
        return emails

    def _create_email(self, mail_id, msg):
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1], _class=EmailMessage)
                return ServerEmail(mail_id, msg)

    def get_folders(self) -> List[Tuple]:

        s, r = self.imap.list()
        if s == 'OK':
            if not self._folders:
                self._folders = [x for x in r]

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

    def is_unread(self, mail_id):
        return mail_id in self._unread_messages
        
    def mark_read(self, mail_id):
        if mail_id in self._unread_messages:
            self._unread_messages.remove(mail_id)
        self.imap.store(mail_id, '+FLAGS', r'\Seen')

    def mark_unread(self, mail_id):
        print("marking unread", mail_id)
        self.imap.store(mail_id, '-FLAGS', r'\Seen')
        self._unread_messages.add(mail_id)

    def get_trash_folder(self):
        for f in self._folders:
            if b'trash' in f[1].lower():
                return f[1].decode().split('"/')[0]


    def mark_deleted(self, mail_id):  # pragma: no cover
        f = self.get_trash_folder()
        print("trash folder:", f)
        if f:
            self.imap.copy(mail_id, f)
            self.imap.store(mail_id, "+FLAGS", r"\Deleted")
            self.imap.expunge()

    def send(self, mail: Email):
        "Send email through mailserver"
        self.server.send_message(mail.getMessage())

    def quit(self):  # pragma: no cover
        "Quit the server"
        self.server.quit()
        self.imap.close()
        self.imap.logout()

