import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt

class BVIDManagerUI(QWidget):
    def __init__(self, bvid_file_path=None, parent=None):
        super().__init__(parent)

        # 默认 BVID 文件路径（项目根目录下）
        self.bvid_file = bvid_file_path or os.path.join(os.path.abspath(os.path.dirname(__file__) + "/.."), "BVID_list.txt")

        self.all_bvids = []
        self.filtered_bvids = []

        self.init_ui()
        self.load_bvids()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 顶部工具栏（搜索 + 添加 + 删除 + 刷新）
        top_bar = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索 BV 号...")
        self.search_box.textChanged.connect(self.filter_bvids)
        top_bar.addWidget(self.search_box)

        self.add_box = QLineEdit()
        self.add_box.setPlaceholderText("输入 BV 号添加")
        top_bar.addWidget(self.add_box)

        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.add_bvid)
        top_bar.addWidget(btn_add)

        btn_delete = QPushButton("删除选中")
        btn_delete.clicked.connect(self.delete_selected)
        top_bar.addWidget(btn_delete)

        btn_refresh = QPushButton("刷新")
        btn_refresh.clicked.connect(self.load_bvids)
        top_bar.addWidget(btn_refresh)

        layout.addLayout(top_bar)

        # 表格区
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["选择", "BV号"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止直接编辑
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

    def load_bvids(self):
        """读取 BVID_list.txt 并显示到表格"""
        if not os.path.exists(self.bvid_file):
            open(self.bvid_file, "w", encoding="utf-8").close()

        with open(self.bvid_file, "r", encoding="utf-8") as f:
            self.all_bvids = [line.strip() for line in f if line.strip()]

        self.filter_bvids()

    def filter_bvids(self):
        """根据搜索框过滤"""
        keyword = self.search_box.text().strip().lower()
        if keyword:
            self.filtered_bvids = [bv for bv in self.all_bvids if keyword in bv.lower()]
        else:
            self.filtered_bvids = list(self.all_bvids)
        self.update_table()

    def update_table(self):
        """刷新表格内容"""
        self.table.setRowCount(len(self.filtered_bvids))
        for row, bv in enumerate(self.filtered_bvids):
            # 选择复选框
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)

            # BV 号
            self.table.setItem(row, 1, QTableWidgetItem(bv))

    def add_bvid(self):
        """添加 BV 号"""
        new_bv = self.add_box.text().strip()
        if not new_bv:
            return
        if new_bv in self.all_bvids:
            QMessageBox.warning(self, "警告", "该 BV 号已存在！")
            return

        self.all_bvids.append(new_bv)
        self.save_bvids()
        self.add_box.clear()
        self.filter_bvids()

    def delete_selected(self):
        """删除选中的 BV 号"""
        selected_bvids = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item.checkState() == Qt.Checked:
                selected_bvids.append(self.table.item(row, 1).text())

        if not selected_bvids:
            QMessageBox.information(self, "提示", "请先勾选要删除的 BV 号")
            return

        self.all_bvids = [bv for bv in self.all_bvids if bv not in selected_bvids]
        self.save_bvids()
        self.filter_bvids()

    def save_bvids(self):
        """保存到文件"""
        with open(self.bvid_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.all_bvids))
