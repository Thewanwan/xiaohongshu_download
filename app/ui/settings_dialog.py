from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox, QSpinBox, QLineEdit, QWidget, QHBoxLayout
from app.config.settings import load_settings, save_settings


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置")
        self.resize(420, 320)

        self.settings = load_settings()

        layout = QVBoxLayout(self)

        self.dir_label = QLabel(self.settings["download_dir"])
        btn_dir = QPushButton("选择下载目录")

        self.log_check = QCheckBox("记录日志")
        self.log_check.setChecked(self.settings["log_enable"])

        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 10)
        self.thread_spin.setValue(self.settings["thread_count"])

        self.advanced_btn = QPushButton("高级设置")
        self.advanced_panel = QWidget()
        adv_layout = QVBoxLayout(self.advanced_panel)

        self.proxy_edit = QLineEdit(self.settings["proxy"])
        adv_layout.addWidget(QLabel("代理"))
        adv_layout.addWidget(self.proxy_edit)

        self.advanced_panel.setVisible(False)

        btn_save = QPushButton("保存")

        layout.addWidget(QLabel("下载目录"))
        layout.addWidget(self.dir_label)
        layout.addWidget(btn_dir)
        layout.addWidget(self.log_check)

        row = QHBoxLayout()
        row.addWidget(QLabel("线程数"))
        row.addWidget(self.thread_spin)
        layout.addLayout(row)

        layout.addWidget(self.advanced_btn)
        layout.addWidget(self.advanced_panel)
        layout.addStretch()
        layout.addWidget(btn_save)

        btn_dir.clicked.connect(self.choose_dir)
        self.advanced_btn.clicked.connect(self.toggle_adv)
        btn_save.clicked.connect(self.save)

    def choose_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            self.dir_label.setText(path)

    def toggle_adv(self):
        self.advanced_panel.setVisible(not self.advanced_panel.isVisible())

    def save(self):
        self.settings["download_dir"] = self.dir_label.text()
        self.settings["log_enable"] = self.log_check.isChecked()
        self.settings["thread_count"] = self.thread_spin.value()
        self.settings["proxy"] = self.proxy_edit.text()
        save_settings(self.settings)
        self.accept()