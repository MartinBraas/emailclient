
from PySide2.QtCore import QModelIndex, QPoint, QRect, QRegExp, QSize
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPen, QRegExpValidator, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListView, QListWidget, QMainWindow, QPushButton, QSizePolicy, QStyle, QStyleOptionViewItem, QStyledItemDelegate, QTextEdit, QVBoxLayout, QWidget


class EmailList(QListView):
    """
    A display for a list of emails
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(1)
        self.setSizePolicy(policy)
        self.setUniformItemSizes(True)
        self.setModel(QStandardItemModel(5, 1))
        self.setItemDelegate(MailItemDelagate(self, self.model()))


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
            mail_item = self.model.data(index);

            unread = True

            # Set the background color
            background = option.palette.highlight() if  (option.state & QStyle.State_Selected) else option.palette.base();

            painter.fillRect(option.rect, background);

            titleRect = option.rect;
            titleRect.setX(titleRect.x()+5);
            titleRect.setWidth(titleRect.x()-5);

            font=painter.font() ;
            font.setPointSize(10);

            # Title
            if unread:
                font.setWeight(QFont.Bold);
            painter.setFont(font);
            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+23), "Tryg");

            if not unread:
                font.setWeight(QFont.Normal);

            # Date
            painter.setFont(font);
            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+43), "12. Dec, 2019");
            

            # Subject

            excerpt = "Hello world hell world wdgfdfgdfshggfdhfdgh fhfdghdfg fghd"

            display_width = self.view.size().width() * 0.2

            if (len(excerpt) > display_width):
                excerpt = excerpt[:int(display_width)-20] + "...";

            painter.drawText(QPoint(option.rect.x()+10, option.rect.y()+65), excerpt);

            painter.fillRect(QRect(
                                    option.rect.x() + option.rect.width() - 60,
                                    option.rect.y(),
                                    60,
                                    option.rect.height()), background);

            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.setBrush(QBrush(QColor(100, 100, 200)))

            painter.drawLine(option.rect.x(), option.rect.y()+option.rect.height(), option.rect.x()+option.rect.width(), option.rect.y()+option.rect.height())

        else:
            return super().paint(painter, option, index)

    def sizeHint(self, option:  QStyleOptionViewItem, index:  QModelIndex) -> QSize:
        return QSize(180, 90)

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

        self.title = QLabel()
        self.title.setText("Test Title")
        f = self.title.font()
        f.setWeight(QFont.Bold)
        self.title.setFont(f)

        self.by = QLabel()
        self.by.setText("<Hello world> test@email")
        layout.addWidget(self.title)
        layout.addWidget(self.by)

        self.body = QTextEdit()
        self.body.setReadOnly(True)
        self.body.setHtml("""
        <div class="context">
<h1 class="title">QTextEdit Class</h1>
<p>The QTextEdit class provides a widget that is used to edit and display both plain and rich text. <a href="#details" data-hydrus="DONE">More...</a></p>
<div class="table"><table class="alignedsummary">
<tbody><tr><td class="memItemLeft rightAlign topAlign"> Header:</td><td class="memItemRight bottomAlign"> <span class="preprocessor">#include &lt;QTextEdit&gt;</span>
</td></tr><tr><td class="memItemLeft rightAlign topAlign"> CMake:</td><td class="memItemRight bottomAlign"> find_package(Qt6 COMPONENTS Widgets REQUIRED) <br>
target_link_libraries(mytarget PRIVATE Qt6::Widgets)</td></tr><tr><td class="memItemLeft rightAlign topAlign"> qmake:</td><td class="memItemRight bottomAlign"> QT += widgets</td></tr><tr><td class="memItemLeft rightAlign topAlign"> Inherits:</td><td class="memItemRight bottomAlign"> <a href="qabstractscrollarea.html" data-hydrus="DONE">QAbstractScrollArea</a></td></tr><tr><td class="memItemLeft rightAlign topAlign"> Inherited By:</td><td class="memItemRight bottomAlign"> <p><a href="qtextbrowser.html" data-hydrus="DONE">QTextBrowser</a></p>
</td></tr></tbody></table></div>
<ul>
<li><a href="qtextedit-members.html" data-hydrus="DONE">List of all members, including inherited members</a></li>
</ul>
<h2 id="public-types">Public Types<a class="plink" href="#public-types" title="Direct link to this headline" data-hydrus="DONE"></a></h2>
<div class="table"><table class="alignedsummary">
<tbody><tr><td class="memItemLeft rightAlign topAlign"> struct </td><td class="memItemRight bottomAlign"><b><a href="qtextedit-extraselection.html" data-hydrus="DONE">ExtraSelection</a></b></td></tr>
<tr><td class="memItemLeft rightAlign topAlign"> flags </td><td class="memItemRight bottomAlign"><b><a href="qtextedit.html#AutoFormattingFlag-enum" data-hydrus="DONE">AutoFormatting</a></b></td></tr>
<tr><td class="memItemLeft rightAlign topAlign"> enum </td><td class="memItemRight bottomAlign"><b><a href="qtextedit.html#AutoFormattingFlag-enum" data-hydrus="DONE">AutoFormattingFlag</a></b> { AutoNone, AutoBulletList, AutoAll }</td></tr>
<tr><td class="memItemLeft rightAlign topAlign"> enum </td><td class="memItemRight bottomAlign"><b><a href="qtextedit.html#LineWrapMode-enum" data-hydrus="DONE">LineWrapMode</a></b> { NoWrap, WidgetWidth, FixedPixelWidth, FixedColumnWidth }</td></tr>
</tbody></table></div>
<h2 id="properties">Properties<a class="plink" href="#properties" title="Direct link to this headline" data-hydrus="DONE"></a></h2>
</div>
        """)
        layout.addWidget(self.body)


class EmailFolderSelector(QComboBox):
    """
    Selection input for different email folders
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.insertItem(0, "Inbox", None)

class MailLayout(QVBoxLayout):
    """
    Layout for displaying mails in a list
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        header_layout = QHBoxLayout()
        self.addLayout(header_layout)

        user_label = QLabel("Face McFaceFace <face@mcface.com>")
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
        email_list_layout.addWidget(self.email_folder_selector)
        email_list_layout.addWidget(self.email_list)
        layout.addLayout(email_list_layout)

        self.email_open = EmailOpen()
        layout.addWidget(self.email_open)

        
class FolderWidget(QWidget):
    """
    Base class for page folder
    """

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.mail_layout = MailLayout(self)

    def connect_buttons(self, main_window):
        self.mail_layout.compose_btn.clicked.connect(main_window.compose_page)


class QLineEditNumber(QLineEdit):
    """
    QLineEdit that only accepts numbers
    """

    def __init__(self, parent: None) -> None:
        super().__init__(parent=parent)

        self.setValidator(QRegExpValidator(QRegExp("[0-9]*")))