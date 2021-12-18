
from typing import List
from PySide2.QtCore import QModelIndex, QObject, QPoint, QRegExp, QSize, QStandardPaths, QThread, Signal, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtGui import QBrush, QColor, QDesktopServices, QFont, QPainter, QPen, QRegExpValidator, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QListView, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QSizePolicy, QStackedWidget, QStyle, QStyleOptionViewItem, QStyledItemDelegate, QTextBrowser, QVBoxLayout, QWidget
from backend import server, variables
from backend import mail
from backend.mail import ServerEmail
from array import array as arr
import os

from ui.compose import ComposeData
from ui.spinner import QtWaitingSpinner

DataRole = Qt.UserRole + 1

class EmailList(QListView):
    """
    A display for a list of emails
    """

    mail_clicked = Signal(ServerEmail)
    load_more_signal = Signal(int, int)
    class LoadMore(QObject):
        loaded_mails = Signal(list)

        def __init__(self) -> None:
            super().__init__()
            self.fetching = False

        def get(self, limit, load_from):
            if not self.fetching:
                print("getting mails", load_from, limit)
                self.fetching = True
                emails = []
                try:
                    if variables.server:
                        emails = variables.server.fetch(limit=limit, start_from=load_from)
                finally:
                    self.loaded_mails.emit(emails)
                    self.fetching = False

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
        self.setMinimumWidth(self.sizeHintForColumn(0))
        self.spin = QtWaitingSpinner(self, disableParentWhenSpinning=True)

        self._thread = QThread(self)
        self._load_more_action = self.LoadMore()
        self._load_more_action.loaded_mails.connect(self.on_mails)
        self._load_more_action.moveToThread(self._thread)
        self.load_more_signal.connect(self._load_more_action.get)
        self.verticalScrollBar().valueChanged.connect(self.on_scroll_value)

    def on_scroll_value(self, v):
        s = self.verticalScrollBar()
        # check if scrolled more than 90%
        if v > s.maximum() * 0.9:
            self.load_more()


    def on_mail_click(self, idx):
        d = self._model.data(idx, DataRole)
        self.mail_clicked.emit(d) 
        print("mail clicked", d) 
        # variables.reply_btn(ServerEmail.get_recipents(d))

    def on_mails(self, mails: List[ServerEmail]):
        # print("received mails", mails)
        for e in mails:
            item = QStandardItem()
            item.setCheckable(False)
            item.setEditable(False)
            item.setData(e, DataRole)
            self._model.appendRow(item)
            self._load_from += 1
        self.spin.stop()

    def load_more(self, limit=20):
        self._thread.start()
        self.spin.start()
        self.load_more_signal.emit(limit, self._load_from)

    def load(self):
        self._model.clear()
        self._load_from = 0
        self.load_more()

    def remove_currently_selected(self):
        self._model.takeRow(self.currentIndex().row())
        d = self._model.data(self.currentIndex(), DataRole)
        self.mail_clicked.emit(d)

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
            painter.save()
            servermail: ServerEmail = self.model.data(index, DataRole);

            unread = variables.server.is_unread(servermail.get_id())

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
            date = servermail.get_date()
            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+43), date[0:22]);
            

            # Subject

            excerpt = servermail.get_subject()

            display_width = self.view.size().width() * 0.2

            if (len(excerpt) > display_width):
                excerpt = excerpt[:int(display_width)-20] + "...";

            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+65), excerpt);  
            painter.restore()
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
    mail_deleted = Signal()
    mail_read = Signal()

    class MailAction(QObject):
        mark_read = Signal(bytes)
        mark_unread = Signal(bytes)
        mark_deleted = Signal(bytes)
        attachment = Signal(str, bytes)
        attachment_downloaded = Signal(str)

        def read_mail(self, mail_id):
            variables.server.mark_read(mail_id)

        def delete_mail(self, mail_id):
            variables.server.mark_deleted(mail_id)

        def unread_mail(self, mail_id):
            variables.server.mark_unread(mail_id)

        def download_attachment(self, name, content):
            print("downliading", name)
            download_folder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
            attempt = 1
            p = os.path.join(download_folder, name)
            # if already exist, generate random name
            while os.path.exists(p):
                p = os.path.join(download_folder, name + f' ({attempt})')
                attempt += 1

            with open(p, "wb") as f:
                f.write(content)
            print("finished", p)
            self.attachment_downloaded.emit(p)

    
    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(3)
        self.setSizePolicy(policy)

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        self.reply_btn = QPushButton("Reply")
        self.reply_btn.setToolTip("Reply to Email")
        self.reply_btn.setDisabled(True)
        header_layout.addWidget(self.reply_btn)

        self.forward_btn = QPushButton("Forward")
        self.forward_btn.setToolTip("Forward Email")
        self.forward_btn.setDisabled(True)
        header_layout.addWidget(self.forward_btn)
        header_layout.insertStretch(-1, 1)


        self.mark_unread_btn = QPushButton("Mark as unread")
        self.mark_unread_btn.setDisabled(True)
        self.mark_unread_btn.setToolTip("Mark as Unread")
        header_layout.addWidget(self.mark_unread_btn)
        self.mark_unread_btn.clicked.connect(self.on_mark_unread)


        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setDisabled(True)
        self.delete_btn.setToolTip("Delete Email")
        header_layout.addWidget(self.delete_btn)
        self.delete_btn.clicked.connect(self.on_delete)

        
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

        self.attachments = QListWidget()
        self.attachments.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.attachments.setMaximumHeight(100)
        self.attachments.setVisible(False)
        self.attachments.itemDoubleClicked.connect(self.download_attachment)
        layout.addWidget(self.attachments)

        self._current_mail = None
        self._current_attachments = []
        self._current_type = ''

        self._mark_read_action = self.MailAction()
        self._thread = QThread(self)
        self._mark_read_action.moveToThread(self._thread)
        self._mark_read_action.mark_read.connect(self._mark_read_action.read_mail)
        self._mark_read_action.mark_deleted.connect(self._mark_read_action.delete_mail)
        self._mark_read_action.mark_unread.connect(self._mark_read_action.unread_mail)
        self._mark_read_action.attachment.connect(self._mark_read_action.download_attachment)
        self._mark_read_action.attachment_downloaded.connect(self.on_attachment_downloaded)
        self._thread.start()

    def download_attachment(self, item: QListWidgetItem):
        name = item.text()
        content = item.data(Qt.UserRole+1)
        print("emitting", name, type(content))
        self._mark_read_action.attachment.emit(name, content)

    def on_attachment_downloaded(self, p):
        print("downloaded", p)
        msg = QMessageBox.information(self, "Attachment download", "Attachment has been downloaded to: " + p, QMessageBox.Ok)

    def on_delete(self):
        if self._current_mail:
            self._mark_read_action.mark_deleted.emit(self._current_mail.get_id())
        self.mail_deleted.emit()
        
    def on_mark_unread(self):
        if self._current_mail:
            self._mark_read_action.mark_unread.emit(self._current_mail.get_id())
            self.mail_read.emit()


    def show_email(self, mail: ServerEmail):
        self.attachments.clear()
        self._current_mail = mail
        body = mail.get_body()
        self.by.setText(mail.get_recipents())
        self.title.setText(mail.get_subject())
        self.show_body(body, mail.get_content_type().lower())
        self._mark_read_action.mark_read.emit(mail.get_id())
        self.mail_read.emit()
        self._current_attachments = mail.get_attachment()
        if self._current_attachments:
            self.attachments.setVisible(True)
        else:
            self.attachments.setVisible(False)
        for name, content in self._current_attachments:
            t = QListWidgetItem(name, self.attachments)
            t.setData(Qt.UserRole+1, content)
            t.setData(Qt.DisplayRole, name)

    def show_body(self, body, type = '', null=False):
        self.forward_btn.setDisabled(False)
        self.delete_btn.setDisabled(False)
        self.reply_btn.setDisabled(False)
        self.mark_unread_btn.setDisabled(False)
        try:
            if 'html' in type:
                print("showing html")
                self.body.setHtml(body)
                self.stack.setCurrentIndex(0)
                self._current_type = 'html'
            else:
                print("showing plain")
                self.body_plain.setText(body)
                self.stack.setCurrentIndex(1)
                self._current_type = 'plain'
        except ValueError:
            if not null:
                self.show_body(body.replace(chr(0), ""), type, True)
            raise

    def get_current_mail(self):
        return self._current_mail

    def get_current_type(self):
        return self._current_type


class EmailFolderSelector(QComboBox):
    """
    Selection input for different email folders
    """

    folder_selected = Signal(str)
    run_get_folders = Signal()

    class GetFolders(QObject):
        folders = Signal(list)

        def get(self):
            print("getting folders")
            l = variables.server.get_folders()
            print(l)
            self.folders.emit(l)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self._thread = QThread(self)
        self._get_folders = self.GetFolders()
        self._get_folders.folders.connect(self.on_folders)
        self.run_get_folders.connect(self._get_folders.get)
        self._get_folders.moveToThread(self._thread)
        self.addItem("Loading...")

        self.currentIndexChanged.connect(self.on_select)

    def on_folders(self, folders):
        self.clear()
        for f in folders:
            self.addItem(f[0], f[0])

    def load(self):
        if variables.server:
            self._thread.start()
            self.run_get_folders.emit()


    def on_select(self, idx):
        if variables.server:
            name = self.itemData(idx)
            if name:
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
        self.compose_btn.setToolTip("Start writing an Email")
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
        self.email_open.mail_deleted.connect(self.email_list.remove_currently_selected)
        layout.addWidget(self.email_open)

    def on_folder_selected(self, f):
        self.email_list.load()

    def load(self):
        self.email_folder_selector.load()

        
class FolderPage(QWidget):
    """
    Base class for page folder
    """

    def __init__(self, main_window) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.mail_layout = MailLayout(self)
        self.email_open = self.mail_layout.email_open

    def connect_buttons(self):
        self.mail_layout.compose_btn.clicked.connect(lambda: self.main_window.compose_page(None))
        self.email_open.reply_btn.clicked.connect(self.on_reply)
        self.email_open.forward_btn.clicked.connect(self.on_forward)

    def on_reply(self):
        current_mail = self.email_open.get_current_mail()
        if current_mail:
            data = ComposeData()
            data.compose_type = "reply"
            data.to = current_mail.get_recipents(include_name=False)
            data.subject = "RE: " + current_mail.get_subject()
            data.type = self.email_open.get_current_type()
            self.main_window.compose_page(data)

    def on_forward(self):
        current_mail = self.email_open.get_current_mail()
        if current_mail:
            data = ComposeData()
            data.compose_type = "forward"
            data.subject =  "FW: " + current_mail.get_subject()
            data.body = current_mail.get_body()
            data.type = self.email_open.get_current_type()
            self.main_window.compose_page(data)

        

    def load(self):
        self.mail_layout.load()

class QLineEditNumber(QLineEdit):
    """
    QLineEdit that only accepts numbers
    """

    def __init__(self, parent: None) -> None:
        super().__init__(parent=parent)

        self.setValidator(QRegExpValidator(QRegExp("[0-9]*")))