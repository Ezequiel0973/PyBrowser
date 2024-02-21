if __name__ == '__main__':

    import sys
    from PyQt6.QtWidgets import QApplication
    from .browser_window import BrowserWindow

    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())