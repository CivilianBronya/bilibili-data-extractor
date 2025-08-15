from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class VideoContentUI(QWidget):
    def __init__(self, bv_id=None):
        super().__init__()
        self.setWindowTitle("查看被提取的视频本体")

        self.bv_id = bv_id
        self.layout = QVBoxLayout(self)

        label = QLabel("🚧 该功能正在开发中，耐心等待更新 🚧")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: #555;")
        self.layout.addWidget(label)
        self.layout.addStretch()
