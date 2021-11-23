from PySide2.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QSpacerItem

from ui.widgets import FolderWidget, MailLayout

class InboxPage(FolderWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)

