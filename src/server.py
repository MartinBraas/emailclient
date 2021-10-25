import smtplib
import imaplib


class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, imapserv, port_w_tls, port) -> None:
        self.host = smtpserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv, port_w_tls, port)
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

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

    def fetch(self, limit=10, folder="INBOX"):
        "Fetch emails"
        status, messages = self.imap.select(folder)
        limit = min(int(messages[0]), limit)
        emails = []
        for i in range(l):
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            emails.append(self._create_email(msg))

        return emails

    def _create_email(self, msg):
        print(msg)
        return
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    # write the file
                    open(filepath, "w").write(body)
                    # open in the default browser
                    webbrowser.open(filepath)

    def folders(self):
        return self.imap.list()

    def send(self, sender, reciepient, emailbody):
        "Send email through mailserver"
        self.server.sendmail(sender, reciepient, emailbody)

    def quit(self):
        "Quit the server"
        self.server.quit()
        self.imap.close()
        self.imap.logout()

