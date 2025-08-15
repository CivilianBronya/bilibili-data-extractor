import os
import multiprocessing
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox
)
from info_start import run_extraction

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extraction_process(bvid_file, output_dir, log_queue):
    def logger(msg):
        log_queue.put(msg)

    run_extraction(
        bvid_file=bvid_file,
        output_dir=output_dir,
        log=logger
    )
    log_queue.put("__FINISHED__")


class ExtractorStartUI(QWidget):
    def __init__(self, bvid_file_path=None,
                 my_message="本软件为开源软件，免费提供使用，若付费取得，那么已经被骗了！ \n本项目软件地址：https://github.com/CivilianBronya/bilibili-data-extractor/"):
        super().__init__()
        self.bvid_file_path = bvid_file_path
        self.my_message = my_message
        self.bvid_list = []

        self.process = None
        self.log_queue = multiprocessing.Queue()

        self.setup_ui()
        self.start_button.clicked.connect(self.start_extraction)
        self.load_bvids()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_log_queue)

    def setup_ui(self):
        self.setWindowTitle("提取开始")
        main_layout = QVBoxLayout(self)

        # BV 号表格
        bvid_label = QLabel("BV号列表")
        bvid_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(bvid_label)

        self.bvid_table = QTableWidget()
        self.bvid_table.setColumnCount(1)
        self.bvid_table.setHorizontalHeaderLabels(["BV号"])
        self.bvid_table.horizontalHeader().setStretchLastSection(True)
        self.bvid_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bvid_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bvid_table.setSelectionMode(QTableWidget.SingleSelection)
        main_layout.addWidget(self.bvid_table)

        # 作者信息
        my_label = QLabel("作者的话")
        my_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(my_label)

        self.my_text = QTextEdit()
        self.my_text.setPlainText(self.my_message)
        self.my_text.setReadOnly(True)
        self.my_text.setFixedHeight(80)
        main_layout.addWidget(self.my_text)

        # 启动按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.start_button = QPushButton("开始提取")
        btn_layout.addWidget(self.start_button)
        main_layout.addLayout(btn_layout)

    def load_bvids(self):
        self.bvid_list.clear()
        if self.bvid_file_path and os.path.exists(self.bvid_file_path):
            with open(self.bvid_file_path, "r", encoding="utf-8") as f:
                self.bvid_list = [line.strip() for line in f if line.strip()]

        self.bvid_table.setRowCount(len(self.bvid_list))
        for row, bvid in enumerate(self.bvid_list):
            self.bvid_table.setItem(row, 0, QTableWidgetItem(bvid))

    def start_extraction(self):
        if not self.bvid_file_path or not os.path.exists(self.bvid_file_path):
            QMessageBox.warning(self, "错误", "未找到 BV 号文件，请先配置 BVID_list.txt")
            return

        output_dir = os.path.join(PROJECT_ROOT, "output")
        os.makedirs(output_dir, exist_ok=True)

        self.start_button.setEnabled(False)
        QMessageBox.information(self, "提示", "提取任务已开始")

        # 启动子进程
        self.process = multiprocessing.Process(
            target=extraction_process,
            args=(self.bvid_file_path, output_dir, self.log_queue)
        )
        self.process.start()
        self.timer.start(100)

    def check_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            if msg == "__FINISHED__":
                self.timer.stop()
                self.process.join()
                self.start_button.setEnabled(True)
                QMessageBox.information(self, "提示", "所有提取任务已完成")
                return
            print(msg)
