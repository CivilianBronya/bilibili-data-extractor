import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_DIR = os.path.join(BASE_DIR, "styles", "images")
logo_path = os.path.join(IMG_DIR, "logo.png")

from gui.ui_main import BilibiliExtractorGUI


def main():
    app = QApplication(sys.argv)

    # 启动画面
    if os.path.exists(logo_path):
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = QSplashScreen(pixmap)
    else:
        print(f"Logo not found: {logo_path}")
        splash = QSplashScreen()

    splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    def start_main():
        splash.close()
        window = BilibiliExtractorGUI()
        window.show()

    QTimer.singleShot(2000, start_main)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
