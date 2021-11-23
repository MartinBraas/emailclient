
from PySide2.QtWidgets import QHBoxLayout, QLabel, QListWidget, QMainWindow, QPushButton, QSizePolicy, QTextEdit, QVBoxLayout, QWidget

class EmailList(QListWidget):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(1)
        self.setSizePolicy(policy)

class EmailOpen(QWidget):
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHorizontalStretch(3)
        self.setSizePolicy(policy)

        layout = QVBoxLayout(self)
        self.title = QLabel()
        self.title.setText("Test Title")
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


class MailLayout(QVBoxLayout):

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        btn_layout = QHBoxLayout()
        self.addLayout(btn_layout)
        self.compose_btn = QPushButton("Compose")
        btn_layout.addWidget(self.compose_btn)
        btn_layout.insertStretch(0, 1)

        layout = QHBoxLayout()
        self.addLayout(layout)

        self.email_list = EmailList()
        layout.addWidget(self.email_list)

        self.email_open = EmailOpen()
        layout.addWidget(self.email_open)

        
class FolderWidget(QWidget):

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.mail_layout = MailLayout(self)

    def connect_buttons(self, main_window):
        self.mail_layout.compose_btn.clicked.connect(main_window.compose_page)