from PySide2.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

from backend import variables
from backend import server as sv
from backend import mail as em

# v = variables
recipient_email = "a"
recipient_name = "a"
mail_subject = "a"
mail_body = "a"

class ComposePage(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)

        layout = QFormLayout(self)

        self.subject = QLineEdit()
        self.to = QLineEdit()
        self.cc = QLineEdit()
        self.body = QTextEdit()

        layout.addRow("Subject:", self.subject)
        layout.addRow("To:", self.to)
        layout.addRow("CC:", self.cc)
        layout.addWidget(self.body)

        
        layout_widget = QWidget()
        btn_layout = QHBoxLayout(layout_widget)
        layout.addWidget(layout_widget)
        self.attachment_btn = QPushButton("Add Attachment")
        self.send_btn = QPushButton("Send")
        btn_layout.addWidget(self.attachment_btn)
        btn_layout.addWidget(self.send_btn)
        btn_layout.insertStretch(1, 1)

    # def send_mail():
    #     server = sv.Server(v.smtp_serv, 0, v.port_w_tls, v.port)
    #     server.connect()

    #     email = em.Email()
    #     with open('../../messages.txt', 'r') as f:
    #         message = f.read()
    #     email.setBody(message)

    #     email.setRecipient(recipient_name, recipient_email)
    #     email.setSubject(mail_subject)
    #     server.login(v.email_adress, v.email_password)
    #     server.send(v.email_adress, recipient_email, email.getString())

    #     server.quit()

