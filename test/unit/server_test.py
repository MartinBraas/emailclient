from unittest.mock import patch
from pprint import pprint
from src.server import Server

# SMTP SERVER
smtpserv = "smtp-mail.outlook.com"
port_w_tls = 587
port = 25
imapserv = "imap-mail.outlook.com"
user = ""
pass_ = ""

@patch('src.server.Server')
def test_server_can_connect(ServerMock):
    server: Server = ServerMock(smtpserv, imapserv, port_w_tls, port)

    # ensure that the info is the same
    assert server.host == smtpserv
    assert server.imap_host == imapserv
    assert server.port_tls == port_w_tls
    assert server.port == port

    # test that the mailserver is connected

def test_server_can_fetch():
    server: Server = Server(smtpserv, imapserv, port_w_tls, port)
    server.connect()
    server.login(user, pass_)
    pprint(server.get_folders())
    mails = server.fetch()
    assert len(mails)