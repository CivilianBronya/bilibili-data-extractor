import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QTextEdit, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def open_with_default_app(path: str):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
    except Exception as e:
        QMessageBox.warning(None, "打开失败", f"无法打开: {path}\n{e}")


class VideoDetailDialog(QDialog):
    """显示指定 BV 文件夹内容"""
    def __init__(self, bvid: str, folder_path: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"视频详情 — {bvid}")
        self.resize(760, 520)
        self.bvid = bvid
        self.folder = folder_path

        layout = QHBoxLayout(self)

        # 左侧：封面
        left = QVBoxLayout()
        cover_label = QLabel()
        cover_label.setAlignment(Qt.AlignCenter)
        cover_label.setFrameShape(QFrame.Box)
        cover_path = self._find_cover_path()

        if cover_path and os.path.exists(cover_path):
            pix = QPixmap(cover_path).scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cover_label.setPixmap(pix)
        else:
            cover_label.setText("未找到封面")
        left.addWidget(cover_label)
        left.addStretch()

        # 右侧：文件信息 + 操作按钮
        right = QVBoxLayout()
        right.addWidget(QLabel(f"BV 目录：{self.folder}"))
        right.addSpacing(6)

        # 弹幕 XML
        danmaku_path = os.path.join(self.folder, "danmaku.xml")
        if os.path.exists(danmaku_path):
            btn_danmaku = QPushButton("查看弹幕 (XML)")
            btn_danmaku.clicked.connect(lambda: self.show_text_file(danmaku_path))
            right.addWidget(btn_danmaku)
        else:
            right.addWidget(QLabel("缺少: 弹幕 XML"))

        # 视频文件
        video_found = False
        for ext in ("mp4", "mkv", "webm", "mov", "flv"):
            for f in os.listdir(self.folder):
                if f.lower().endswith("." + ext):
                    btn_video = QPushButton(f"播放视频 ({f})")
                    btn_video.clicked.connect(lambda _, pp=os.path.join(self.folder, f): open_with_default_app(pp))
                    right.addWidget(btn_video)
                    video_found = True
                    break
            if video_found:
                break
        if not video_found:
            right.addWidget(QLabel("缺少: 视频文件"))

        # 音频文件
        audio_found = False
        for ext in ("mp3", "m4a", "aac", "wav"):
            for f in os.listdir(self.folder):
                if f.lower().endswith("." + ext):
                    btn_audio = QPushButton(f"播放音频 ({f})")
                    btn_audio.clicked.connect(lambda _, pp=os.path.join(self.folder, f): open_with_default_app(pp))
                    right.addWidget(btn_audio)
                    audio_found = True
                    break
            if audio_found:
                break
        if not audio_found:
            right.addWidget(QLabel("缺少: 音频文件"))

        # 打开整个文件夹
        btn_open_folder = QPushButton("打开此 BV 文件夹")
        btn_open_folder.clicked.connect(lambda: open_with_default_app(self.folder))
        right.addSpacing(8)
        right.addWidget(btn_open_folder)

        # 关闭
        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.close)
        right.addStretch()
        right.addWidget(btn_close)

        layout.addLayout(left, 1)
        layout.addLayout(right, 1)

    def _find_cover_path(self):
        for ext in ("cover.jpg", "cover.jpeg", "cover.png", "cover.webp"):
            p = os.path.join(self.folder, ext)
            if os.path.exists(p):
                return p
        # 返回任意图片
        for f in os.listdir(self.folder):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                return os.path.join(self.folder, f)
        return None

    def show_text_file(self, path: str):
        if not os.path.exists(path):
            QMessageBox.warning(self, "文件不存在", path)
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f"查看 {os.path.basename(path)}")
        dlg.resize(600, 400)
        layout = QVBoxLayout(dlg)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        with open(path, "r", encoding="utf-8") as f:
            text_edit.setPlainText(f.read())
        layout.addWidget(text_edit)
        dlg.exec_()


class VideoShowUI(QWidget):
    """主界面：扫描 output/ 下的 BV 子文件夹"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("已爬取视频浏览")
        self.resize(980, 560)

        layout = QVBoxLayout(self)

        # 顶部按钮
        top_row = QHBoxLayout()
        self.btn_refresh = QPushButton("刷新列表")
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_open_output = QPushButton("打开 output 文件夹")
        self.btn_open_output.clicked.connect(lambda: open_with_default_app(OUTPUT_DIR))
        top_row.addWidget(self.btn_refresh)
        top_row.addWidget(self.btn_open_output)
        top_row.addStretch()
        layout.addLayout(top_row)

        # 表格
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["BV号", "已包含文件", "查看"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        if not os.path.exists(OUTPUT_DIR):
            self.status_label.setText(f"未找到 output 目录：{OUTPUT_DIR}")
            return

        entries = [d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]
        entries.sort()
        if not entries:
            self.status_label.setText("output 文件夹中还没有已提取的视频。")
            return
        self.status_label.setText(f"找到 {len(entries)} 个已提取的视频文件夹")

        for row, folder_name in enumerate(entries):
            folder_path = os.path.join(OUTPUT_DIR, folder_name)
            files = os.listdir(folder_path)
            summary = ", ".join([f for f in files if len(f) <= 30])
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(folder_name))
            self.table.setItem(row, 1, QTableWidgetItem(summary))

            btn_view = QPushButton("查看")
            btn_view.clicked.connect(lambda _, b=folder_name, p=folder_path: self.show_detail(b, p))
            self.table.setCellWidget(row, 2, btn_view)

    def show_detail(self, bvid: str, folder_path: str):
        dlg = VideoDetailDialog(bvid, folder_path, parent=self)
        dlg.exec_()

    def refresh_video_list(self):
        self.refresh_table()