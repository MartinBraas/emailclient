from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from ui.compose import ComposePage
from ui.inbox import InboxPage

from ui.login import LoginPage

class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Skrumpen Email Client")
        self.resize(900, 700)


    def login_page(self):
        page = LoginPage(self)
        page.login_btn.clicked.connect(self.inbox_page)
        self.setCentralWidget(page)

    def inbox_page(self):
        page = InboxPage(self)
        page.connect_buttons(self)
        self.setCentralWidget(page)

    def compose_page(self):
        page = ComposePage(self)
        self.setCentralWidget(page)

