import os
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

from backend import mail as em, variables

from dataclasses import dataclass

@dataclass
class ComposeData:
    compose_type = 'reply' # reply or forward
    subject: str = ''
    to: str = ''
    cc: str = ''
    bcc: str = ''
    body: str = ''
    attachments = None
class ComposePage(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.setWindowTitle("Compose")

        layout = QFormLayout(self)

        self.subject = QLineEdit()
        self.to = QLineEdit()
        self.cc = QLineEdit()
        self.bcc = QLineEdit()
        self.body = QTextEdit()

        layout.addRow("Subject:", self.subject)
        layout.addRow("To:", self.to)
        layout.addRow("CC:", self.cc)
        layout.addRow("BCC:", self.bcc)
        layout.addWidget(self.body)
        
        layout_widget = QWidget()
        btn_layout = QHBoxLayout(layout_widget)

        self.attachments = QListWidget()
        self.attachments.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.attachments.setMaximumHeight(100)
        self.attachments.setVisible(False)
        self.attachments.itemDoubleClicked.connect(self.on_remove_attachment)
        layout.addWidget(self.attachments)

        layout.addWidget(layout_widget)

        self.attachment_btn = QPushButton("Add Attachment")
        self.attachment_btn.clicked.connect(self.on_add_attachment)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.on_send)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(lambda:self.close())
        btn_layout.addWidget(self.close_btn)
        btn_layout.addWidget(self.attachment_btn)
        btn_layout.addWidget(self.send_btn)
        btn_layout.insertStretch(1, 1)

        self.files = set()

    def on_add_attachment(self):
        files = QFileDialog.getOpenFileNames(self, "Select one or more attachments")
        for f in files[0]:
            self.attachments.setVisible(True)
            self.files.add(f)
        self.update_attachments()        

    def update_attachments(self):
        self.attachments.clear()
        for f in self.files:
            name = os.path.split(f)[1]
            print(name)
            t = QListWidgetItem(name, self.attachments)
            t.setData(Qt.UserRole+1, f)
            t.setData(Qt.DisplayRole, name)

    def on_remove_attachment(self, item):
        f = item.data(Qt.UserRole+1)
        self.files.remove(f)
        self.update_attachments()

    def set_data(self, data: ComposeData):
        self.to.setText(data.to)
        self.cc.setText(data.cc)
        self.bcc.setText(data.bcc)
        self.subject.setText(data.subject)
        self.body.setText(data.body)
        self.set_newline()
        if data.compose_type == 'reply':
            self.body.setFocus(Qt.OtherFocusReason)
        elif data.compose_type == 'forward':
            self.to.setFocus(Qt.OtherFocusReason)
    
    def set_newline(self):
        t = self.body.textCursor()
        t.setPosition(0)
        self.body.setTextCursor(t)
        self.body.insertHtml("<br/><hr/><br/>")
        t = self.body.textCursor()
        t.setPosition(0)
        self.body.setTextCursor(t)

    def clear(self):
        self.files = set()
        self.update_attachments()
        self.subject.setText("")
        self.to.setText("")
        self.cc.setText("")
        self.bcc.setText("")
        self.body.setText("")
        self.attachments.setVisible(False)

    def on_send(self):
        mail = em.Email()
        mail.setBody(self.body.toHtml(), "html")
        mail.setSubject(self.subject.text())
        mail.setRecipient(variables.email_adress, self.to.text())
        mail.setCC(self.cc.text())
        mail.setBCC(self.bcc.text())

        # attachments
        for f in self.files:
            if os.path.exists(f) and not os.path.isdir(f):
                with open(f, 'rb') as r:
                    mail.addAttachment(os.path.split(f)[1], r.read())

        try:
            variables.server.send(mail)

            msg = QMessageBox()
            msg.setWindowTitle("Mail sent")
            msg.setText("Email has been successfully sent")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(lambda: self.close())
            x = msg.exec_()
        except Exception as e:
            if 'connect()' in str(e):
                variables.server.connect()
                return self.on_send()
            msg = QMessageBox()
            msg.setWindowTitle("An error occurred")
            msg.setText(str(e))
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

    def closeEvent(self, event) -> None:
        self.clear()
        return super().closeEvent(event)