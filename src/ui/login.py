from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QLineEdit, QFormLayout
from PySide2.QtCore import QSize, QThread, Qt, Signal, QObject
from backend import utils, variables
from backend import server as sv
from backend import mail as em
from ui.collapse import CollapeWidget
from ui.spinner import QtWaitingSpinner
from ui.widgets import QLineEditNumber
import traceback

v = variables

class LoginAction(QThread):
    login_result = Signal(bool, str)

    def __init__(self, page) -> None:
        super().__init__()
        self.page = page


    def run(self): # pragma: no cover
        print("logging in")
        if self.save_smtp():
            self.save_login()

    def save_smtp(self): # pragma: no cover
        email = self.page.email.text()
        advanced_imap = self.page.imap_serv.text()
        advanced_imap_port = self.page.imap_port.text()
        advanced_smtp = self.page.smtp_serv.text()
        advanced_port_tls = self.page.port_w_tls.text()
        advanced_port = self.page.port.text()
        #Autodetection to be implemented after advanced page
        if "@gmail" in email:
            v.choose_smtp(1, " ", 0, 0)
            v.choose_imap(1, " ", 0)
        elif "@outlook" in email or "@hotmail" in email or "@live" in email:
            v.choose_smtp(0, " ", 0, 0)
            v.choose_imap(0, " ", 0)
        else:
            v.choose_smtp(2, advanced_smtp, advanced_port_tls, advanced_port)
            v.choose_imap(2, advanced_imap, advanced_imap_port)

        try:
            print("smtp server", v.smtp_serv)
            print("imap server", v.imap_serv)
            v.server = sv.Server(v.smtp_serv, v.imap_serv, v.port_w_tls, v.port)
            v.server.connect()
            return True
        except Exception as e:
            traceback.print_exc()
            msg = str(e)
            self.login_result.emit(False, msg)
            return False

    def save_login(self): # pragma: no cover
        email = self.page.email.text()
        password = self.page.password.text()
        v.load_login(email, password)
        try:
            if v.server:
                v.server.login(email, password)
            msg = ""
            self.login_result.emit(True, msg)
        except Exception as e:
            traceback.print_exc()
            msg = str(e)
            self.login_result.emit(False, msg)


class LoginPage(QWidget):

    login_signal = Signal(bool, str)

    def __init__(self, parent = None):
        super().__init__(parent=parent)

        main_layout = QVBoxLayout(self)

        img = QPixmap(utils.resource_path("images/logo.png"))
        img_lbl = QLabel()
        img_lbl.setPixmap(img)
        img_lbl.setScaledContents(True)
        img_lbl.setMinimumWidth(img.width()*0.8)
        img_lbl.setMinimumHeight(img.height()*0.8)
        img_layout = QHBoxLayout()
        img_layout.addWidget(img_lbl)
        img_layout.insertStretch(0)
        img_layout.insertStretch(-1)

        main_layout.addLayout(img_layout)

        layout = QHBoxLayout()
        main_layout.addLayout(layout)
        v_layout = QVBoxLayout()
        form_layout = QFormLayout()
        layout.addLayout(v_layout)


        self.email = QLineEdit(self)
        self.email.setMinimumWidth(300)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.imap_serv = QLineEdit(self)
        self.imap_port = QLineEditNumber(self)
        self.imap_port.setMinimumWidth(100)
        self.smtp_serv = QLineEdit(self)
        self.smtp_serv.setMinimumWidth(300)
        self.port = QLineEditNumber(self)
        self.port.setMinimumWidth(100)
        self.port_w_tls = QLineEditNumber(self)
        self.port_w_tls.setMinimumWidth(100)

        self.email.setText("")
        self.email.setPlaceholderText("Email")
        self.password.setText("")
        self.password.setPlaceholderText("Password")

        self.message_label = QLabel()
        self.message_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")

        form_layout.addRow("Email:", self.email)
        form_layout.addRow("Password", self.password)
        v_layout.addLayout(form_layout)

        advanced_widget = QWidget()
        advanced_layout = QFormLayout(advanced_widget)

        collapse = CollapeWidget(self, "Advanced")
        collapse.addWidget(advanced_widget)
        v_layout.addWidget(collapse)

        advanced_layout.addRow("SMTP Server", self.smtp_serv)
        advanced_layout.addRow("SMTP Port", self.port)
        advanced_layout.addRow("SMTP Port with TLS", self.port_w_tls)
        advanced_layout.addRow("IMAP Server", self.imap_serv)
        advanced_layout.addRow("IMAP Port", self.imap_port)

        loginbtn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.on_login_clicked)
        loginbtn_layout.addWidget(self.login_btn)
        loginbtn_layout.insertStretch(0)

        v_layout.addLayout(loginbtn_layout)
        v_layout.addWidget(self.message_label)
        self.spin = QtWaitingSpinner(self, disableParentWhenSpinning=True)
        v_layout.addWidget(self.spin)

        # center widgets vertically and horizontally

        layout.insertStretch(0, 1)
        layout.insertStretch(-1, 1)
        v_layout.insertStretch(0, 1)
        v_layout.insertStretch(-1, 1)

        #
        self.email.textChanged.connect(self.on_email_text_change)
        self.login_signal.connect(self.on_login_signal)

    def on_login_clicked(self):
        self.spin.start()
        self.login_action = LoginAction(self)
        self.login_action.login_result.connect(self.login_signal.emit)
        self.login_action.start()

    def on_login_signal(self, status, msg):
        if not status:
            self.message_label.setText(msg)
            self.spin.stop()

    def on_email_text_change(self, txt):
        smtp_serv = port_w_tls = port = None
        imap_serv = imap_port = None

        if "@gmail" in txt:
            smtp_serv, port_w_tls, port = v.choose_smtp(1, " ", 0, 0)
            imap_serv, imap_port = v.choose_imap(1, " ", 0)
        elif "@outlook" in txt or "@hotmail" in txt or "@live" in txt:
            smtp_serv, port_w_tls, port = v.choose_smtp(0, " ", 0, 0)
            imap_serv, imap_port = v.choose_imap(0, " ", 0)

        if smtp_serv:
            self.smtp_serv.setPlaceholderText(smtp_serv)
            self.port_w_tls.setPlaceholderText(str(port_w_tls))
            self.port.setPlaceholderText(str(port))

        if imap_serv:
            self.imap_serv.setPlaceholderText(imap_serv)
            self.imap_port.setPlaceholderText(str(imap_port))

