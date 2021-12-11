from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout
from PySide2.QtCore import Signal
from PySide2.QtGui import QPixmap
from backend import variables
from backend import server as sv
from backend import mail as em
from ui.widgets import QLineEditNumber
import traceback

v = variables

class LoginPage(QWidget):

    login_signal = Signal(bool, str)

    def __init__(self, parent = None):
        super().__init__(parent=parent)

        layout = QHBoxLayout(self)
        v_layout = QVBoxLayout()
        form_layout = QFormLayout()
        layout.addLayout(v_layout)

        self.email = QLineEdit(self)
        self.email.setMinimumWidth(300)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.smtp_serv = QLineEdit(self)
        self.smtp_serv.setMinimumWidth(300)
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
        form_layout.addRow("SMTP Server", self.smtp_serv)
        form_layout.addRow("Port with TLS", self.port_w_tls)

        loginbtn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.function_calls)
        loginbtn_layout.addWidget(self.login_btn)
        loginbtn_layout.insertStretch(0)

        v_layout.addLayout(form_layout)
        v_layout.addLayout(loginbtn_layout)
        v_layout.addWidget(self.message_label)

        # center widgets vertically and horizontally

        layout.insertStretch(0, 1)
        layout.insertStretch(-1, 1)
        v_layout.insertStretch(0, 1)
        v_layout.insertStretch(-1, 1)

        #
        self.email.textChanged.connect(self.on_email_text_change)

    def on_email_text_change(self, txt):
        smtp_serv = port_w_tls = port = None

        if "@gmail" in txt:
            smtp_serv, port_w_tls, port = v.choose_smtp(1, " ", 0)
            v.choose_imap(1, " ", 0)
        elif "@outlook" in txt or "@hotmail" in txt or "@live" in txt:
            smtp_serv, port_w_tls, port = v.choose_smtp(0, " ", 0)
            v.choose_imap(0, " ", 0)

        if smtp_serv:
            self.smtp_serv.setPlaceholderText(smtp_serv)
            self.port_w_tls.setPlaceholderText(str(port_w_tls))

        

        

    def function_calls(self):
        if self.save_smtp():
            self.save_login()
        # self.tell_em()

    # def tell_em(self):
        # smtp_serv = self.smtp_serv
        # port_w_tls = self.port_w_tls
        # print("Smtp server:", self.smtp_serv.text(), " // Port with TLS: ", self.port_w_tls.text())
        # print("Email adress: ", self.email.text(), " // Password: ", self.password.text())

    def save_smtp(self):
        email = self.email.text()
        advanced_smtp = self.smtp_serv.text()
        advanced_port = self.port_w_tls.text()
        #Autodetection to be implemented after advanced page
        if "@gmail" in email:
            v.choose_smtp(1, " ", 0)
            v.choose_imap(1, " ", 0)
        elif "@outlook" in email or "@hotmail" in email or "@live" in email:
            v.choose_smtp(0, " ", 0)
            v.choose_imap(0, " ", 0)
        else:
            v.choose_smtp(2, advanced_smtp, advanced_port)

        try:
            v.server = sv.Server(v.smtp_serv, v.imap_serv, v.port_w_tls, v.port)
            v.server.connect()
            return True
        except Exception as e:
            traceback.print_exc()
            msg = str(e)
            self.login_signal.emit(False, msg)
            self.message_label.setText(msg)
            return False

    def save_login(self):
        email = self.email.text()
        password = self.password.text()
        v.load_login(email, password)
        try:
            if v.server:
                v.server.login(email, password)
            msg = ""
            self.login_signal.emit(True, msg)
        except Exception as e:
            traceback.print_exc()
            msg = str(e)
            self.login_signal.emit(False, msg)

        self.message_label.setText(msg)