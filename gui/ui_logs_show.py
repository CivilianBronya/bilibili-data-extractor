from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LogsShowUI(QWidget):
    def __init__(self, parent=None, log_file_path=None):
        super().__init__(parent)
        self.log_file_path = log_file_path or os.path.join(BASE_DIR, "logs.txt")

        # 主布局
        layout = QVBoxLayout(self)

        # 日志显示框
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("刷新日志")
        self.refresh_btn.clicked.connect(self.load_logs)
        btn_layout.addWidget(self.refresh_btn)

        layout.addLayout(btn_layout)

    def load_logs(self):
        """加载日志文件内容"""
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, "r", encoding="utf-8", errors="ignore") as f:
                self.text_edit.setPlainText(f.read())
        else:
            self.text_edit.setPlainText("日志文件不存在：\n" + self.log_file_path)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # 创建 LogsShowUI
        self.page_logs_show = LogsShowUI()
        self.stack.addWidget(self.page_logs_show)  # index 0

        btn = QPushButton("切换日志页")
        btn.clicked.connect(self.show_logs_manager)
        layout.addWidget(btn)

    def show_logs_manager(self):
        self.page_logs_show.load_logs()
        self.stack.setCurrentWidget(self.page_logs_show)
