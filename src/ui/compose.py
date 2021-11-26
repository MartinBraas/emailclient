from PySide2.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

from backend import variables, server

class ComposePage(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)

        layout = QFormLayout(self)

        self.subject = QLineEdit()
        self.to = QLineEdit()
        self.cc = QLineEdit()
        self.cc.text()
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

