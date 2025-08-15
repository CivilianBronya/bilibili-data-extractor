import os
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QStackedWidget
)
from PyQt5.QtCore import Qt, QPoint
from gui.ui_bvid_manager import BVIDManagerUI
from gui.ui_extractor_start import ExtractorStartUI
from gui.ui_excel_show import ExcelShowUI
from gui.ui_logs_show import LogsShowUI
from gui.ui_video_data import VideoDataWidget
from gui.ui_video_show import VideoShowUI
from gui.ui_video_content import VideoContentUI


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QSS_DIR = os.path.join(BASE_DIR, "styles", "qss")
IMG_DIR = os.path.join(BASE_DIR, "styles", "images")


class StyleSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(200, 120)

        layout = QVBoxLayout(self)

        # 顶部栏 + 关闭按钮
        top_layout = QHBoxLayout()
        self.title_label = QLabel("选择界面样式")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(
            "QPushButton { border: none; background: none; font-size: 14px; }"
            "QPushButton:hover { color: red; }"
        )
        close_btn.clicked.connect(self.close)

        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(close_btn)
        layout.addLayout(top_layout)

        # 样式单选按钮
        self.radio_group = QButtonGroup(self)
        self.light_btn = QRadioButton("Light 主题")
        self.dark_btn = QRadioButton("Dark 主题")
        layout.addWidget(self.light_btn)
        layout.addWidget(self.dark_btn)

        self.radio_group.addButton(self.light_btn)
        self.radio_group.addButton(self.dark_btn)

        self.light_btn.setChecked(True)  # 默认 light

    def popup(self, pos: QPoint):
        self.move(pos)
        self.show()

    def apply_theme(self, qss):
        self.setStyleSheet(qss)

    def mousePressEvent(self, event):
        event.accept()  # 阻止事件传到主窗口


class BilibiliExtractorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bilibili 视频信息提取器 - GUI 测试版")
        self.resize(1200, 700)

        self.default_theme = os.path.join(QSS_DIR, "light.qss")
        self.current_theme = self.default_theme

        self.style_selector = StyleSelector(self)

        # 主内容区使用 QStackedWidget
        self.stack = QStackedWidget()
        self.page_placeholder = QLabel("点击左侧边栏的文字打开分类界面\n\n目前功能继续完善与开发")
        self.page_placeholder.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(self.page_placeholder)  # index 0

        # 创建 BVIDManager 页面
        self.page_bvid_manager = BVIDManagerUI(
            bvid_file_path=os.path.join(BASE_DIR, "BVID_list.txt")
        )
        self.stack.addWidget(self.page_bvid_manager)  # index 1

        self.page_logs_show = LogsShowUI(

        )
        self.stack.addWidget(self.page_logs_show)  # index 2

        # 创建 ExtractorStart 页面
        self.page_extractor_start = ExtractorStartUI(
            bvid_file_path=os.path.join(BASE_DIR, "BVID_list.txt")
        )
        self.stack.addWidget(self.page_extractor_start)  # index 3

        # 创建 VideoContentUI 页面
        self.page_video_data_manager = VideoDataWidget()
        self.stack.addWidget(self.page_video_data_manager)  # index 4

        # 创建 VideoContentUI 页面
        self.page_video_content = VideoContentUI()
        self.stack.addWidget(self.page_video_content)  # index 5

        # 创建 VideoShowUI 页面
        self.page_video_show = VideoShowUI()
        self.stack.addWidget(self.page_video_show)  # index 6

        # 创建 ExcelShowUI 页面
        self.page_excel_show = ExcelShowUI()
        self.stack.addWidget(self.page_excel_show)  # index 7
        self.init_ui()

        # 默认加载
        self.apply_stylesheet(self.default_theme)

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # 顶部栏
        top_bar = QHBoxLayout()
        title_label = QLabel("Bilibili 视频信息提取器 - GUI 测试版")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        version_label = QLabel("Version: ui.beta-0.26   Author: 星丶白羽莲")
        version_label.setStyleSheet("font-size: 14px;")

        title_container = QVBoxLayout()
        title_container.addWidget(title_label)
        title_container.addWidget(version_label)

        style_btn = QPushButton("界面样式选择")
        style_btn.setFixedHeight(50)
        style_btn.clicked.connect(self.show_style_selector)

        top_bar.addLayout(title_container)
        top_bar.addStretch()
        top_bar.addWidget(style_btn)

        top_frame = QFrame()
        top_frame.setLayout(top_bar)
        top_frame.setFrameShape(QFrame.Box)
        main_layout.addWidget(top_frame)

        # 主体
        body_layout = QHBoxLayout()

        # 左侧栏
        sidebar_layout = QVBoxLayout()
        self.sidebar_buttons = [
            ("准备 - B站视频BV号", self.show_bvid_manager),
            ("日志 - 专业人士专用", self.show_logs_manager),
            ("开始 - 小视频大调查", self.show_extractor_start_manager),
            ("数据 - 视频各类信息", self.show_video_data_manager),
            ("内容 - 提取视频本体", self.show_video_content_manager),
            ("查看 - 数据信息表格", self.show_excel_manager),
            ("查看 - 已下载的视频", self.show_video_manager)
        ]
        for text, action in self.sidebar_buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(action)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar_layout)
        sidebar_frame.setFixedWidth(250)

        # 主内容区（stacked widget）
        content_frame = QFrame()
        content_frame.setLayout(QVBoxLayout())
        content_frame.layout().addWidget(self.stack)

        body_layout.addWidget(sidebar_frame)
        body_layout.addWidget(content_frame)
        main_layout.addLayout(body_layout)

    def show_bvid_manager(self):
        # 切换到 BVIDManager 页面并刷新
        self.page_bvid_manager.load_bvids()
        self.stack.setCurrentWidget(self.page_bvid_manager)

    def show_logs_manager(self):
        # 切换到 LogsShowUI 页面并刷新
        self.page_logs_show.load_logs()
        self.stack.setCurrentWidget(self.page_logs_show)

    def show_extractor_start_manager(self):
        # 切换到 ExtractorStart 页面并刷新
        self.page_extractor_start.load_bvids()
        self.stack.setCurrentWidget(self.page_extractor_start)

    def show_video_data_manager(self):
        # 切换到VideoDataWidget 页面并刷新
        self.stack.setCurrentWidget(self.page_video_data_manager)

    def show_video_content_manager(self):
        # 切换到 VideoContentUI 页面并刷新
        self.stack.setCurrentWidget(self.page_video_content)

    def show_excel_manager(self):
        # 切换到 ExcelShowUI 页面并刷新
        self.page_excel_show.refresh_data()
        self.stack.setCurrentWidget(self.page_excel_show)

    def show_video_manager(self):
        # 切换到 VideoShowUI 页面并刷新
        self.page_video_show.refresh_video_list()
        self.stack.setCurrentWidget(self.page_video_show)

    def set_content_text(self, text):
        # 设置占位页面文字
        self.page_placeholder.setText(text)
        self.stack.setCurrentWidget(self.page_placeholder)

    def load_theme(self, qss_file):
        try:
            with open(qss_file, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            QMessageBox.warning(self, "样式文件缺失", f"未找到 {qss_file}，将使用默认样式。")
            self.setStyleSheet("QWidget { background-color: white; color: black; }")

    def show_style_selector(self):
        btn_pos = self.mapToGlobal(self.rect().topRight()) - QPoint(220, -40)
        self.style_selector.popup(btn_pos)

        # 绑定主题切换
        self.style_selector.light_btn.toggled.connect(
            lambda checked: self.change_theme(os.path.join(QSS_DIR, "light.qss")) if checked else None
        )
        self.style_selector.dark_btn.toggled.connect(
            lambda checked: self.change_theme(os.path.join(QSS_DIR, "dark.qss")) if checked else None
        )

    def change_theme(self, theme_file):
        self.current_theme = theme_file
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                qss = f.read()
                self.setStyleSheet(qss)
                self.style_selector.apply_theme(qss)
        except FileNotFoundError:
            QMessageBox.warning(self, "样式文件缺失", f"未找到 {theme_file}，将使用默认样式。")
            default_qss = "QWidget { background-color: white; color: black; }"
            self.setStyleSheet(default_qss)
            self.style_selector.apply_theme(default_qss)

    def set_content_text(self, text):
        self.content_label.setText(text)

    def mousePressEvent(self, event):
        if self.style_selector.isVisible() and not self.style_selector.geometry().contains(event.globalPos()):
            self.style_selector.close()
        super().mousePressEvent(event)

    def apply_stylesheet(self, file_path):
        self.load_theme(file_path)
