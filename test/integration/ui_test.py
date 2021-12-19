import os
import sys
from PySide2.QtWidgets import QApplication
import pytest
from unittest.mock import MagicMock


from PySide2.QtCore import Qt

# makes it possible to import modules
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../..', 'src')))

from src.backend import variables
from src.ui import login, compose
from src.ui.login import LoginPage
from src.backend.mail import ServerEmail
from src.ui.pages import MainWindow
from src.ui.widgets import FolderPage
from src.ui.compose import ComposePage

def test_ui_login_success(mocker, qtbot):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    mocker.patch('PySide2.QtWidgets.QApplication')
    from main import main
    # ensure can run without raising any errors
    main()

    win = MainWindow()
    win.login_page()
    # make sure it really is the loginpage
    assert type(win.centralWidget()).__name__ == LoginPage.__name__

    # input details
    loginpage: LoginPage = win.centralWidget()
    qtbot.keyClicks(loginpage.email, "test@test.com")
    qtbot.keyClicks(loginpage.password, "test123")
    assert loginpage.email.text() == 'test@test.com'
    assert loginpage.password.text() == 'test123'

    # assert loginpage.email.text() == 'test'
    def on_login_signal(status, msg):
        return status

    # login was successful
    with qtbot.waitSignal(loginpage.login_signal, raising=True, check_params_cb=on_login_signal, timeout=10000) as blocker:
        qtbot.mouseClick(loginpage.login_btn, Qt.LeftButton)

def test_ui_login_fail(mocker, qtbot):
    s = mocker.patch('src.backend.server.smtplib.SMTP')
    s.configure_mock(**{
        'login': Exception
    })
    mocker.patch('imaplib.IMAP4_SSL')

    win = MainWindow()
    win.login_page()
    # make sure it really is the loginpage
    assert type(win.centralWidget()).__name__ == LoginPage.__name__

    # input details
    loginpage: LoginPage = win.centralWidget()
    qtbot.keyClicks(loginpage.email, "test@test.com")
    qtbot.keyClicks(loginpage.password, "test123")
    

    # assert loginpage.email.text() == 'test'
    def on_login_signal(status, msg):
        assert login.v.server
        return status

    # login failed
    with qtbot.waitSignal(loginpage.login_signal, raising=True, check_params_cb=on_login_signal, timeout=3000) as blocker:
        qtbot.mouseClick(loginpage.login_btn, Qt.LeftButton)

@pytest.fixture()
def fake_server_mails():
    mails = []
    for x in range(10):
        m: ServerEmail = MagicMock()
        m.get_id.return_value = b'123'
        m.get_subject.return_value = "hello world"
        m.get_body.return_value = "<html><body>hello world</body></html>"
        m.get_content_type.return_value = 'text/html'
        m.get_content_disposition.return_value = 'text/html'
        m.get_attachment.return_value = [('dfgdfg', b'fdgdfg')]
        m.get_date.return_value = "feb 20122"
        m.get_recipents.return_value = "hello <ok@ok.com>"
        mails.append(m)

    yield mails


def test_ui_inbox_list(mocker, qtbot, fake_server_mails):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    win = MainWindow()
    win.inbox_page()
    inbox: FolderPage = win.centralWidget()
    inbox.mail_layout.email_list.on_mails(fake_server_mails)
    assert inbox.mail_layout.email_list._model.rowCount() == 10

def test_ui_inbox_open(mocker, qtbot, fake_server_mails):
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    win = MainWindow()
    win.inbox_page()
    inbox: FolderPage = win.centralWidget()
    inbox.mail_layout.email_open.show_email(fake_server_mails[0])

    # # functionality of buttons
    qtbot.mouseClick(inbox.email_open.reply_btn, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(inbox.email_open.forward_btn, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(inbox.email_open.mark_unread_btn, Qt.MouseButton.LeftButton)

def test_ui_compose(mocker, qtbot, monkeypatch):
    monkeypatch.setattr(compose, "QMessageBox", MagicMock())
    mocker.patch('smtplib.SMTP')
    mocker.patch('imaplib.IMAP4_SSL')
    wid = ComposePage()
    wid.clear()
    qtbot.addWidget(wid)
    assert wid.body.toPlainText() == ''
    assert not wid.attachments.isVisible()
    qtbot.keyClicks(wid.to, "test@test.com")
    qtbot.keyClicks(wid.subject, "hello world")
    qtbot.keyClicks(wid.cc, "ok@ok.com")
    qtbot.keyClicks(wid.bcc, "ok@ok.com")
    qtbot.keyClicks(wid.body, "hmmm hmmm")
    wid.update_attachments()
    qtbot.mouseClick(wid.send_btn, Qt.MouseButton.LeftButton)
