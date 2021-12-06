from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from ui.compose import ComposePage
from ui.inbox import InboxPage

from ui.login import LoginPage

class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Skrumpen Email Client")
        self.resize(1200, 800)
        self.compose_window = None


    def login_page(self):
        page = LoginPage(self)
        page.login_btn.clicked.connect(self.inbox_page)
        self.setCentralWidget(page)

    def inbox_page(self):
        page = InboxPage(self)
        page.connect_buttons(self)
        self.setCentralWidget(page)

    def compose_page(self):
        self.compose_window = ComposePage()
        self.compose_window.resize(1000, 800)
        self.compose_window.show()
        # self.setCentralWidget(page)

    def closeEvent(self, event: QCloseEvent) -> None:
        # save work

        if self.compose_window:
            self.compose_window.close()
        event.accept()

