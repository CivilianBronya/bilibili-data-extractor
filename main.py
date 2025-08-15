import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "styles", "images")


from gui.ui_main import BilibiliExtractorGUI


def main():
    app = QApplication(sys.argv)

    # 启动画面
    logo_path = os.path.join(IMG_DIR, "logo.png")
    splash = QSplashScreen(QPixmap(logo_path)) if os.path.exists(logo_path) else QSplashScreen()
    splash.setWindowFlags(Qt.FramelessWindowHint)
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
