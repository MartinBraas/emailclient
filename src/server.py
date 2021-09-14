import smtplib


class Server:
    """
    A class encapsulating a mail server
    """

    def __init__(self, smtpserv, port_w_tls, port) -> None:
        self.host = smtpserv
        self.port_tls = port_w_tls
        self.port = port

        self.server = smtplib.SMTP(smtpserv, port_w_tls, port)

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

    def send(self, sender, reciepient, emailbody):
        "Send email through mailserver"
        self.server.sendmail(sender, reciepient, emailbody)

    def quit(self):
        "Quit the server"
        self.server.quit()
