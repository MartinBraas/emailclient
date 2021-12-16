from PySide2.QtCore import Slot
from PySide2.QtGui import QCloseEvent, QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from ui.compose import ComposeData, ComposePage
import sys

from ui.login import LoginPage
from ui.widgets import FolderPage


def setIcon(widget):
    appIcon = QIcon("images/icon_png-removebg-preview.png")
    widget.setWindowIcon(appIcon)
class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Skrumpen Email Client")
        self.resize(1200, 800)
        self.compose_window = None
        setIcon(self)

    def login_page(self):
        page = LoginPage(self)
        page.login_signal.connect(self.on_login)
        self.setCentralWidget(page)

    def on_login(self, success, msg):
        if success:
            p = self.inbox_page()
            p.load()

    def inbox_page(self):
        page = FolderPage(self)
        page.connect_buttons()
        self.setCentralWidget(page)
        return page

    def compose_page(self, data: ComposeData = ComposeData()):
        if not self.compose_window:
            self.compose_window = ComposePage()
            self.compose_window.resize(1000, 800)
        if data:
            self.compose_window.set_data(data)
        self.compose_window.show()
        setIcon(self.compose_window)

    def closeEvent(self, event: QCloseEvent) -> None:
        # save work

        if self.compose_window:
            self.compose_window.close()
        event.accept()
