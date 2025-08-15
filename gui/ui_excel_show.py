import os
import datetime
import subprocess
import sys
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class ExcelShowUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Excel & BV 数据统计")
        self.resize(480, 400)

        layout = QVBoxLayout(self)

        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.output_dir = os.path.join(self.root_dir, "output")
        self.excel_path = os.path.join(self.root_dir, "output.xlsx")

        self.label_count = QLabel()
        self.label_today_count = QLabel()
        self.label_last_bv = QLabel()
        self.label_excel_rows = QLabel()
        self.label_excel_last = QLabel()
        self.label_last_time = QLabel()
        self.label_output_size = QLabel()
        self.label_excel_path = QLabel(f"目标 Excel 文件路径: {self.excel_path}")

        self.btn_refresh = QPushButton("刷新统计")
        self.btn_refresh.clicked.connect(self.refresh_data)

        self.btn_open_excel = QPushButton("打开 Excel 表格")
        self.btn_open_excel.clicked.connect(self.open_excel_file)

        # BV 基础信息
        bv_layout = QVBoxLayout()
        bv_layout.addWidget(self.label_count)
        bv_layout.addWidget(self.label_today_count)
        bv_layout.addWidget(self.label_last_bv)
        bv_layout.addWidget(self.label_last_time)

        # Excel 信息
        excel_layout = QVBoxLayout()
        excel_layout.addWidget(self.label_excel_rows)
        excel_layout.addWidget(self.label_excel_last)
        excel_layout.addWidget(self.label_excel_path)

        # 输出文件夹信息
        output_layout = QVBoxLayout()
        output_layout.addWidget(self.label_output_size)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_open_excel)

        # 主布局
        layout.addLayout(bv_layout)
        layout.addSpacing(8)
        layout.addLayout(excel_layout)
        layout.addSpacing(8)
        layout.addLayout(output_layout)
        layout.addSpacing(12)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 初次刷新数据
        self.refresh_data()

    def refresh_data(self):
        bv_folders = [f for f in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, f))] if os.path.exists(self.output_dir) else []

        # BV 统计
        total_bv_count = len(bv_folders)
        today_count = len([f for f in bv_folders if datetime.datetime.fromtimestamp(
            os.path.getmtime(os.path.join(self.output_dir, f))).date() == datetime.date.today()])
        last_bv = max(bv_folders, key=lambda f: os.path.getmtime(os.path.join(self.output_dir, f)), default="无记录")
        last_time = self.get_last_extract_time()

        self.label_count.setText(f"已提取 BV 文件夹总数: {total_bv_count}")
        self.label_today_count.setText(f"今日新增 BV 文件夹数量: {today_count}")
        self.label_last_bv.setText(f"最近提取的 BV: {last_bv}")
        self.label_last_time.setText(f"最近提取时间: {last_time}")

        # Excel 统计
        total_excel_rows = self.count_excel_rows()
        excel_last = datetime.datetime.fromtimestamp(os.path.getmtime(self.excel_path)).strftime("%Y-%m-%d %H:%M:%S") \
            if os.path.exists(self.excel_path) else "无记录"

        self.label_excel_rows.setText(f"Excel 中数据行数: {total_excel_rows}")
        self.label_excel_last.setText(f"Excel 最近修改时间: {excel_last}")

        # 输出目录大小
        total_size = self.get_dir_size(self.output_dir) if os.path.exists(self.output_dir) else 0
        self.label_output_size.setText(f"output 文件夹总大小: {self.format_size(total_size)}")

    def count_excel_rows(self):
        if not os.path.exists(self.excel_path):
            return 0
        try:
            df = pd.read_excel(self.excel_path)
            return len(df)
        except Exception:
            return 0

    def get_last_extract_time(self):
        if not os.path.exists(self.output_dir):
            return "无记录"
        bv_folders = [f for f in os.listdir(self.output_dir) if os.path.isdir(os.path.join(self.output_dir, f))]
        if not bv_folders:
            return "无记录"
        latest_folder = max((os.path.join(self.output_dir, f) for f in bv_folders), key=os.path.getmtime)
        ts = os.path.getmtime(latest_folder)
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def get_dir_size(self, path):
        total = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return total

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"

    def open_excel_file(self):
        if os.path.exists(self.excel_path):
            if os.name == "nt":
                os.startfile(self.excel_path)
            elif os.name == "posix":
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", self.excel_path])
        else:
            self.label_excel_path.setText("Excel 文件不存在！")
