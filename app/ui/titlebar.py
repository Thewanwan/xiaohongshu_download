from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint
from app.ui.settings_dialog import SettingsDialog


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(45)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)

        self.icon_label = QLabel("🎨")
        self.title_label = QLabel("小红书图文解析工具")
        self.title_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")

        self.btn_setting = QPushButton("⚙")
        self.btn_min = QPushButton("—")
        self.btn_close = QPushButton("✕")

        btn_style = """
            QPushButton { border: none; background: transparent; font-size: 14px; width: 35px; height: 35px; border-radius: 17px;}
            QPushButton:hover { background-color: #f3f4f6; }
        """

        self.btn_setting.setStyleSheet(btn_style)
        self.btn_min.setStyleSheet(btn_style)
        self.btn_close.setStyleSheet(btn_style + "QPushButton:hover { background-color: #fee2e2; color: #ef4444; }")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.btn_setting)
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_close)

        self.btn_setting.clicked.connect(self.open_settings)
        self.btn_min.clicked.connect(self.do_minimize)
        self.btn_close.clicked.connect(self.parent.close)

    def open_settings(self):
        SettingsDialog().exec()

    def do_minimize(self):
        self.parent.setWindowState(Qt.WindowMinimized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self.parent, 'old_pos'):
            delta = QPoint(event.globalPosition().toPoint() - self.parent.old_pos)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.old_pos = event.globalPosition().toPoint()