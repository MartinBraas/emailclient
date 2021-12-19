from unittest.mock import MagicMock, Mock, patch
from pprint import pprint
import pytest

# SMTP SERVER
smtpserv = "smtp-mail.outlook.com"
port_w_tls = 587
port = 25
imapserv = "imap-mail.outlook.com"
user = "test"
pass_ = "test"

def test_server_can_connect(mocker):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    from src.backend.server import Server
    server = Server(smtpserv, imapserv, port_w_tls, port)

    # ensure that the info is the same
    assert server.host == smtpserv
    assert server.imap_host == imapserv
    assert server.port_tls == port_w_tls
    assert server.port == port

    # test that the mailserver cant login before connecting
    server.login(user, pass_)
    server.server.login.assert_not_called()

    # test that the mailserver is connected
    server.connect()
    server.server.connect.assert_called_once()

    # test mail process is started
    server.server.ehlo.assert_called()

    # test can login
    server.login(user, pass_)
    server.server.login.assert_called_once_with("test", "test")

    # sanity check
    with pytest.raises(AssertionError):
        server.server.login.assert_called_once_with("test", "t2323est")

def test_server_can_select_folder(mocker):
    mocker.patch('smtplib.SMTP')
    m = mocker.patch('imaplib.IMAP4_SSL')
    from src.backend.server import Server
    server = Server(smtpserv, imapserv, port_w_tls, port)
    server.imap.configure_mock(**{
        'select': lambda f: ("OK", ["2323"]),
    })
    server._folders = [("hello", b"f"), ("world", b"df")]
    server.select_folder("yes")
    server.select_folder("hello")


def test_server_can_fetch(mocker):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    from src.backend.server import Server
    server = Server(smtpserv, imapserv, port_w_tls, port)
    server.imap.configure_mock(**{
        'select': lambda f: ("OK", ["2323"]),
        "fetch": MagicMock(return_value=("OK", "")),
        "search": MagicMock(return_value=("OK", ["1 2 3 4 5 6 7 8 9 10"]))
    })
    server._message_count = 10
    server._create_email = MagicMock(return_value=Mock())
    server.fetch(10, 0)
    
def test_server_get_folders(mocker):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    from src.backend.server import Server
    server = Server(smtpserv, imapserv, port_w_tls, port)
    server.imap.configure_mock(**{
        "list": MagicMock(return_value=("OK", b'inbox "/" 22, trash "/" df, draft "/" 11'.split(b',')))
    })
    assert len(server.get_folders()) == 3
    