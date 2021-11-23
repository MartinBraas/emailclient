from PySide2.QtWidgets import QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

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

