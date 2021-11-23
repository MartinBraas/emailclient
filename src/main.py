import sys
from PySide2.QtWidgets import QApplication

from ui.pages import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.login_page()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()