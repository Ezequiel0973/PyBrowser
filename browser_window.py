from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTabWidget, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QUrl


class BrowserWindow(QTabWidget):

    def __init__(self):
        super().__init__()

        # Set window initial properties
        self.setWindowTitle("PyBrowser")
        self.setGeometry(0, 0, 800, 600)
        self.tab_count = 1

        # Configure tab closing buttons
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setStyleSheet('QTabBar::close-button {image: url(icons/close.png);}')

        # Configure first tab
        self.addTab(self.BrowserTab(self), 'New Tab')

    def open_new_tab(self):
        self.addTab(self.BrowserTab(self), 'New Tab')
        self.tab_count += 1

    def open_new_window(self):
        new_window = BrowserWindow()
        new_window.show()

    def close_tab(self, index):
        # Handle tab close action
        tab_to_remove = self.widget(index)
        if tab_to_remove is not None:
            if self.tab_count > 1:
                # Simply remove the tab
                self.removeTab(index)
                tab_to_remove.deleteLater()
                self.tab_count -= 1
            else:
                # Close the window
                self.close()


    class BrowserTab(QWidget):

        def __init__(self, browser_window):
            super().__init__()
            self.browser_window = browser_window

            # Set tab layout
            layout = QVBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)

            # Add a tool bar to tab layout
            tool_bar = QWidget()
            tool_bar.setMaximumHeight(40)
            tool_bar.setStyleSheet('border-top: 2px solid silver; border-bottom: 2px solid silver;')
            layout.addWidget(tool_bar)

            # Set Web content view
            self.web_view = QWebEngineView()
            self.web_view.setUrl(QUrl('https://duckduckgo.com'))
            layout.addWidget(self.web_view)

            # Configure tool bar buttons and url bar
            return_button = self.ToolBarButton('icons/arrow_left.png', self.web_view.back)
            go_button = self.ToolBarButton('icons/arrow_right.png', self.web_view.forward)
            refresh_button = self.ToolBarButton('icons/refresh.png', self.web_view.reload)

            menu_button = self.MenuButton(self)

            self.url_bar = self.UrlBar(self)

            # Add buttons and url bar to tool bar layout
            tool_bar_layout = QHBoxLayout(tool_bar)

            tool_bar_layout.addWidget(return_button)
            tool_bar_layout.addWidget(go_button)
            tool_bar_layout.addWidget(refresh_button)
            tool_bar_layout.addWidget(self.url_bar)
            tool_bar_layout.addWidget(menu_button)

        def navigate(self, url):

            # Add 'http://' to the url if not present
            if not url.startswith("http://"):
                url = "http://" + url
                self.url_bar.setText(url)

            # Update url in respective url bar
            self.web_view.setUrl(QUrl(url))


        class ToolBarButton(QPushButton):

            def __init__(self, icon_path, function):
                super().__init__()

                # Set button style
                self.setStyleSheet('border: 0px solid white')
                self.setIcon(QIcon(icon_path))

                # Apply specified function to the button when pressed
                self.clicked.connect(function)


        class MenuButton(QPushButton):

            def __init__(self, browser_tab):
                super().__init__()

                # Set button style
                self.setStyleSheet('border: 0px solid white')
                self.setIcon(QIcon('icons/menu.png'))

                # Create a QMenu and add actions
                menu = QMenu(self)
                open_new_tab = QAction("Open New Tab", self)
                open_new_window = QAction("Open New Window", self)

                menu.addAction(open_new_tab)
                menu.addAction(open_new_window)

                # Connect actions to slots
                open_new_tab.triggered.connect(browser_tab.browser_window.open_new_tab)
                open_new_window.triggered.connect(browser_tab.browser_window.open_new_window)

                # Set the menu as the button's menu
                self.setMenu(menu)


        class UrlBar(QLineEdit):

            def __init__(self, browser_tab):
                super().__init__()

                # Set url bar properties
                self.browser_tab = browser_tab
                self.setStyleSheet('border-bottom: 0px; border-top: 1px solid silver; border-left: 1px solid silver;')

            def keyPressEvent(self, event):
                super().keyPressEvent(event)

                # Call navigate method from parent BrowserWindow if Enter/Return is pressed
                key = event.key()
                if key == Qt.Key.Key_Enter or key == Qt.Key.Key_Return:
                    self.browser_tab.navigate(self.text())