import sys
import os
from PySide2.QtWidgets import QApplication

from ui.pages import MainWindow

style_path = "style/Devsion.qss"

def main():
    app = QApplication(sys.argv)

    # if os.path.exists(style_path):
    #     with open(style_path, 'r') as f:
    #         app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.login_page()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()