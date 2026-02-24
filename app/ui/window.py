from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QFrame, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from app.ui.titlebar import CustomTitleBar
from app.worker.downloader import Worker


class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 560)

        self.last_was_progress = False
        self.task_index = 0

        self.main_container = QFrame(self)
        self.main_container.setObjectName("MainContainer")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_container)

        content_layout = QVBoxLayout(self.main_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        content_layout.addWidget(self.title_bar)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(25, 20, 25, 25)
        body_layout.setSpacing(15)

        top = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("在此粘贴小红书笔记链接...")
        self.btn = QPushButton("开始下载")
        self.btn.setFixedWidth(120)
        top.addWidget(self.input)
        top.addWidget(self.btn)

        self.progress = QProgressBar()

        card = QFrame()
        card.setObjectName("LogCard")
        card_layout = QVBoxLayout(card)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        card_layout.addWidget(self.log)

        body_layout.addLayout(top)
        body_layout.addWidget(self.progress)
        body_layout.addWidget(card)
        body_layout.setStretchFactor(card, 1)
        content_layout.addWidget(body)

        self.setMinimumSize(640, 460)

        self.setStyleSheet("""
            #MainContainer { background-color: #f3f4f6; border-radius: 12px; border: 1px solid #e5e7eb; }
            QLineEdit { background: white; border: 2px solid #e5e7eb; border-radius: 10px; padding: 10px; font-size: 13px; }
            QLineEdit:focus { border: 2px solid #facc15; }
            QPushButton { background-color: #facc15; border-radius: 10px; padding: 10px; font-weight: bold; color: #422006; }
            QPushButton:hover { background-color: #fde047; }
            QPushButton:disabled { background-color: #e5e7eb; color: #9ca3af; }
            #LogCard { background-color: white; border-radius: 12px; border: 1px solid #e5e7eb; }
            QTextEdit { background: transparent; border: none; font-family: 'Consolas', 'Microsoft YaHei'; color: #374151; }
            QProgressBar { background: #e5e7eb; border-radius: 6px; text-align: center; height: 10px; font-size: 10px;}
            QProgressBar::chunk { background: #3b82f6; border-radius: 6px; }
        """)

        self.btn.clicked.connect(self.start)
        self.input.returnPressed.connect(self.start)

    def _insert_new_line_if_needed(self, cursor):
        if self.log.toPlainText():
            cursor.insertBlock()

    def add_log(self, msg):
        cursor = self.log.textCursor()
        cursor.movePosition(QTextCursor.End)

        if msg.startswith("LOG_UPDATE:"):
            display_msg = msg.replace("LOG_UPDATE:", "")

            if self.last_was_progress:
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.removeSelectedText()
            else:
                self._insert_new_line_if_needed(cursor)

            cursor.insertText(display_msg)
            self.last_was_progress = True
        else:
            self._insert_new_line_if_needed(cursor)
            cursor.insertText(msg)
            self.last_was_progress = False

        self.log.setTextCursor(cursor)
        self.log.ensureCursorVisible()

    def update_progress(self, i, total):
        self.progress.setMaximum(total)
        self.progress.setValue(i)

    def start(self):
        url = self.input.text().strip()
        if not url:
            return

        self.task_index += 1

        cursor = self.log.textCursor()
        cursor.movePosition(QTextCursor.End)

        if self.log.toPlainText():
            cursor.insertBlock()

        cursor.insertText(f"──────── 任务 {self.task_index} ────────")
        cursor.insertBlock()
        cursor.insertBlock()

        self.log.setTextCursor(cursor)
        self.last_was_progress = False

        self.btn.setEnabled(False)
        self.progress.setValue(0)

        self.worker = Worker(url)
        self.worker.log_signal.connect(self.add_log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished.connect(lambda: self.btn.setEnabled(True))
        self.worker.start()
