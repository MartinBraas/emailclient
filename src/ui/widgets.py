
from typing import List
from PySide2.QtCore import QModelIndex, QPoint, QRegExp, QSize, Signal, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtGui import QBrush, QColor, QDesktopServices, QFont, QPainter, QPen, QRegExpValidator, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QListView, QPushButton, QSizePolicy, QStackedWidget, QStyle, QStyleOptionViewItem, QStyledItemDelegate, QTextBrowser, QVBoxLayout, QWidget
from backend import server, variables
from backend.mail import ServerEmail

DataRole = Qt.UserRole + 1

class EmailList(QListView):
    """
    A display for a list of emails
    """

    mail_clicked = Signal(ServerEmail)

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(1)
        self.setSizePolicy(policy)
        self.setUniformItemSizes(True)
        self._model = QStandardItemModel(0, 1)
        self.setModel(self._model)
        self.setItemDelegate(MailItemDelagate(self, self.model()))
        self._load_from = 0
        self.clicked.connect(self.on_mail_click)

    def on_mail_click(self, idx):
        d = self._model.data(idx, DataRole)
        self.mail_clicked.emit(d)
        print("mail clicked", d)

    def load_more(self, limit=20):
        if variables.server:
            items = []
            emails: List[ServerEmail] = variables.server.fetch(limit=limit, start_from=self._load_from)
            for e in emails:
                item = QStandardItem()
                item.setCheckable(False)
                item.setEditable(False)
                item.setData(e, DataRole)
                items.append(item)
                self._model.appendRow(item)

    def load(self):
        self._model.clear()
        self._load_from = 0
        self.load_more()

class MailItemDelagate(QStyledItemDelegate):
    """
    Draws a single mail item
    """

    def __init__(self, view: QListView, model: QStandardItemModel, parent = None) -> None:
        super().__init__(parent=parent)
        self.checked = False
        self.view = view
        self.model = model

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        if index.column() == 0:
            servermail: ServerEmail = self.model.data(index, DataRole);

            unread = not servermail.is_read()

            padding = 2

            # Set the background color
            background = option.palette.highlight() if  (option.state & QStyle.State_Selected) else option.palette.base();

            painter.fillRect(option.rect, background);

            painter.save()

            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.setBrush(QBrush(QColor(100, 100, 200)))

            painter.drawLine(option.rect.x(), option.rect.y()+option.rect.height()-padding, option.rect.x()+option.rect.width(), option.rect.y()+option.rect.height()-padding)

            painter.restore()

            titleRect = option.rect;
            titleRect.setX(titleRect.x()+5);
            titleRect.setWidth(titleRect.x()-5);

            font=painter.font() ;
            font.setPointSize(10);

            # Title
            if unread:
                font.setWeight(QFont.Bold);
            painter.setFont(font);
            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+23), servermail.get_recipents().split("<")[0]);

            if not unread:
                font.setWeight(QFont.Normal);

            # Date
            painter.setFont(font);
            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+43), "12. Dec, 2019");
            

            # Subject

            excerpt = servermail.get_subject()

            display_width = self.view.size().width() * 0.2

            if (len(excerpt) > display_width):
                excerpt = excerpt[:int(display_width)-20] + "...";

            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+65), excerpt);

        else:
            return super().paint(painter, option, index)

    def sizeHint(self, option:  QStyleOptionViewItem, index:  QModelIndex) -> QSize:
        return QSize(180, 90)

class EmailPage(QWebEnginePage):

    def acceptNavigationRequest(self, qurl, navtype, mainframe):
        if navtype != QWebEnginePage.NavigationType.NavigationTypeTyped:
            QDesktopServices.openUrl(qurl)
            return False
        return super().acceptNavigationRequest(qurl, navtype, mainframe)

class EmailOpen(QWidget):
    """
    Widget for reading an email
    """
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(3)
        self.setSizePolicy(policy)

        layout = QVBoxLayout(self)


        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        self.reply_btn = QPushButton("Reply")
        header_layout.addWidget(self.reply_btn)
        self.forward_btn = QPushButton("Forward")
        header_layout.addWidget(self.forward_btn)
        header_layout.insertStretch(-1, 1)

        
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hline)

        info_layout = QFormLayout()
        layout.addLayout(info_layout)

        self.title = QLabel()
        self.title.setText("")
        f = self.title.font()
        f.setWeight(QFont.Bold)
        self.title.setFont(f)

        self.by = QLabel()
        self.by.setText("")
        info_layout.addRow(self.title)
        info_layout.addRow("From:", self.by)
        info_layout.addRow("CC:", QLabel(''))

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hline)

        
        self.body = EmailPage()
        self.body_plain = QTextBrowser()
        view = QWebEngineView()
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setPage(self.body)
        self.stack = QStackedWidget()
        self.stack.addWidget(view)
        self.stack.addWidget(self.body_plain)
        layout.addWidget(self.stack)

    def show_email(self, mail: ServerEmail):
        body = mail.get_body()
        self.by.setText(mail.get_recipents())
        self.title.setText(mail.get_subject())
        self.show_body(body, mail.get_content_type().lower())

    def show_body(self, body, type = '', null=False):
        try:
            if 'html' in type:
                print("showing html")
                self.body.setHtml(body)
                self.stack.setCurrentIndex(0)
            else:
                print("showing plain")
                self.body_plain.setText(body)
                self.stack.setCurrentIndex(1)
        except ValueError:
            if not null:
                self.show_body(body.replace(chr(0), ""), type, True)
            raise


class EmailFolderSelector(QComboBox):
    """
    Selection input for different email folders
    """

    folder_selected = Signal(str)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.currentIndexChanged.connect(self.on_select)

    def load(self):
        if variables.server:
            for f in variables.server.get_folders():
                self.addItem(f[0], f[0])


    def on_select(self, idx):
        if variables.server:
            name = self.itemData(idx)
            variables.server.select_folder(name)
            self.setItemText(idx, f"{name} ({variables.server.get_message_count()})")
            self.folder_selected.emit(name)

class MailLayout(QVBoxLayout):
    """
    Layout for displaying mails in a list
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        header_layout = QHBoxLayout()
        self.addLayout(header_layout)

        user_label = QLabel(variables.email_adress)
        f = user_label.font()
        f.setPointSize(11)
        f.setWeight(QFont.Bold)
        user_label.setFont(f)
        header_layout.addWidget(user_label)

        self.compose_btn = QPushButton("Compose")
        header_layout.addWidget(self.compose_btn)
        header_layout.insertStretch(1, 1)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.addWidget(hline)

        layout = QHBoxLayout()
        self.addLayout(layout)

        email_list_layout = QVBoxLayout()
        self.email_list = EmailList()
        self.email_folder_selector = EmailFolderSelector()
        self.email_folder_selector.folder_selected.connect(self.on_folder_selected)
        email_list_layout.addWidget(self.email_folder_selector)
        email_list_layout.addWidget(self.email_list)
        layout.addLayout(email_list_layout)

        self.email_open = EmailOpen()
        self.email_list.mail_clicked.connect(self.email_open.show_email)
        layout.addWidget(self.email_open)

    def on_folder_selected(self, f):
        self.email_list.load()

    def load(self):
        self.email_folder_selector.load()

        
class FolderWidget(QWidget):
    """
    Base class for page folder
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.mail_layout = MailLayout(self)

    def connect_buttons(self, main_window):
        self.mail_layout.compose_btn.clicked.connect(main_window.compose_page)

    def load(self):
        self.mail_layout.load()

class QLineEditNumber(QLineEdit):
    """
    QLineEdit that only accepts numbers
    """

    def __init__(self, parent: None) -> None:
        super().__init__(parent=parent)

        self.setValidator(QRegExpValidator(QRegExp("[0-9]*")))