from unittest.mock import patch

from src.server import Server

# SMTP SERVER
smtpserv = "smtp-mail.outlook.com"
port_w_tls = 587
port = 25


@patch('src.server.Server')
def test_server_can_connect(ServerMock):
    server: Server = ServerMock(smtpserv, port_w_tls, port)

    # ensure that the info is the same
    assert server.host == smtpserv
    assert server.port_tls == port_w_tls
    assert server.port == port

    # test that the mailserver is connected
