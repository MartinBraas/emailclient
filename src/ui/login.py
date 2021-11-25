from tkinter.constants import E
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem
from backend import variables
from backend import server as sv
from backend import mail as em

v = variables

class LoginPage(QWidget):
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
        self.port_w_tls = QLineEdit(self)
        self.port_w_tls.setMinimumWidth(100)

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

        # center widgets vertically and horizontally

        layout.insertStretch(0, 1)
        layout.insertStretch(-1, 1)
        v_layout.insertStretch(0, 1)
        v_layout.insertStretch(-1, 1)

    def function_calls(self):
        self.save_login()
        self.save_smtp()
        # self.tell_em()

    # def tell_em(self):
        # smtp_serv = self.smtp_serv
        # port_w_tls = self.port_w_tls
        # print("Smtp server:", self.smtp_serv.text(), " // Port with TLS: ", self.port_w_tls.text())
        # print("Email adress: ", self.email.text(), " // Password: ", self.password.text())

    def save_smtp(self):
        global advanced_smtp, advanced_port
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

    def save_login(self):
        global email, password
        email = self.email.text()
        password = self.password.text()
        v.load_login(email, password)
        