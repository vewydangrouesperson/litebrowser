import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget, QHBoxLayout

from PyQt5.QtWebEngineWidgets import QWebEngineView

class CustomTabBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        self.add_tab_button = QPushButton("+")
        layout.addWidget(self.add_tab_button)

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Add initial tab
        self.add_tab()

        # Set custom tab bar
        self.custom_tab_bar = CustomTabBar()
        self.custom_tab_bar.add_tab_button.clicked.connect(self.add_tab)
        self.central_widget.setCornerWidget(self.custom_tab_bar, Qt.TopLeftCorner)

    def add_tab(self):
        tab_index = self.central_widget.count()
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)

        # Entry widget to input URL
        entry = QLineEdit()
        layout.addWidget(entry)

        # Button to open URL
        open_button = QPushButton("SEARCH")
        open_button.clicked.connect(lambda: self.open_url(entry))
        layout.addWidget(open_button)

        # Sidebar layout for navigation buttons
        sidebar_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.central_widget.currentWidget().findChild(QWebEngineView).back())
        sidebar_layout.addWidget(back_button)

        forward_button = QPushButton("Forward")
        forward_button.clicked.connect(lambda: self.central_widget.currentWidget().findChild(QWebEngineView).forward())
        sidebar_layout.addWidget(forward_button)

        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(lambda: self.central_widget.currentWidget().findChild(QWebEngineView).reload())
        sidebar_layout.addWidget(reload_button)

        # Add sidebar to main layout
        layout.addLayout(sidebar_layout)

        # QWebEngineView to display web content
        web_view = QWebEngineView()
        layout.addWidget(web_view)

        self.central_widget.addTab(new_tab, f"Tab {tab_index + 1}")
        self.central_widget.setCurrentIndex(tab_index)

    def open_url(self, entry):
        search_query = entry.text()
        if search_query.strip() != '':
            # Construct the Google search URL
            url = QUrl(f"https://www.google.com/search?q={search_query}")
            web_view = self.central_widget.currentWidget().findChild(QWebEngineView)
            web_view.setUrl(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())