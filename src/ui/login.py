from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

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

        form_layout.addRow("Email:", self.email)
        form_layout.addRow("Password", self.password)

        loginbtn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        loginbtn_layout.addWidget(self.login_btn)
        loginbtn_layout.insertStretch(0)

        v_layout.addLayout(form_layout)
        v_layout.addLayout(loginbtn_layout)

        # center widgets vertically and horizontally
        
        layout.insertStretch(0, 1)
        layout.insertStretch(-1, 1)
        v_layout.insertStretch(0, 1)
        v_layout.insertStretch(-1, 1)
