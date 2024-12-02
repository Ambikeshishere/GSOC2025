import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QHBoxLayout, QTabWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtGui import QIcon


class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, ad_domains):
        super().__init__()
        self.ad_domains = ad_domains

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        for domain in self.ad_domains:
            if domain in url:
                print(f"Blocked: {url}")
                info.block(True)
                return


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ad_domains = self.load_ad_domains()
        self.bookmarks = []
        self.init_ui()

    def init_ui(self):
        # Ad Blocker
        profile = QWebEngineProfile.defaultProfile()
        ad_blocker = AdBlocker(self.ad_domains)
        profile.setRequestInterceptor(ad_blocker)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.add_new_tab)
        self.setCentralWidget(self.tabs)

        # Add initial tab
        self.add_new_tab(QUrl("https://ambikeshishere.github.io/Landing-page/"), "Home")

        # URL Bar (Search Bar)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Search or enter a URL")
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #3E3E3E;
                background-color: #2C2C2C;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 16px;
                color: #FFFFFF;
            }
            QLineEdit:focus {
                background-color: #3A3A3A;
                border-color: #FFFFFF;
            }
        """)

        # Toolbar Buttons
        self.back_button = self.create_toolbar_button("⬅", "Back", self.navigate_back)
        self.forward_button = self.create_toolbar_button("➡", "Forward", self.navigate_forward)
        self.refresh_button = self.create_toolbar_button("⟳", "Refresh", self.reload_page)
        self.home_button = self.create_toolbar_button("🏠", "Home", self.go_home)
        self.bookmarks_button = self.create_toolbar_button("★", "Bookmarks", self.show_bookmarks)
        self.new_tab_button = self.create_toolbar_button("➕", "New Tab", lambda: self.add_new_tab())

        # Toolbar Layout
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        toolbar_layout.addWidget(self.back_button)
        toolbar_layout.addWidget(self.forward_button)
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addWidget(self.home_button)
        toolbar_layout.addWidget(self.bookmarks_button)
        toolbar_layout.addWidget(self.url_bar)
        toolbar_layout.addWidget(self.new_tab_button)

        toolbar = QWidget()
        toolbar.setLayout(toolbar_layout)
        toolbar.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #1E1E1E, stop:1 #333333
            );
            border-bottom: 2px solid #444444;
            border-radius: 12px;
        """)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Window Properties
        self.setWindowTitle("Stark Browser")
        self.setWindowIcon(QIcon("icon.png"))  # Replace with a custom browser icon if available
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QTabWidget::pane { border: 1px solid #444; border-radius: 12px; }
            QTabBar::tab {
                background: #1E1E1E;
                color: #E0E0E0;
                padding: 8px 16px;
                border: 1px solid #444;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: #333333;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)

    def create_toolbar_button(self, text, tooltip, callback):
        button = QPushButton(text)
        button.setToolTip(tooltip)
        button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #2C2C2C;
                border-radius: 10px;
                padding: 6px 10px;
                color: #FFFFFF;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        button.clicked.connect(callback)
        return button

    def load_ad_domains(self):
        return [
            "doubleclick.net",
            "adservice.google.com",
            "googlesyndication.com",
            "ads.pubmatic.com",
            "amazon-adsystem.com",
            "adroll.com",
            "taboola.com"
        ]

    def add_new_tab(self, url=None, label="New Tab"):
        browser = QWebEngineView()

        # Enable JavaScript
        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # Set initial URL
        homepage = QUrl("https://ambikeshishere.github.io/Landing-page/")
        browser.setUrl(url if url else homepage)
        browser.urlChanged.connect(lambda new_url: self.update_url_bar(new_url, browser))
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            url = self.url_bar.text().strip()
            if "." in url and not url.startswith("http"):  # Likely a URL
                url = "https://" + url
            elif not "." in url:  # Search query
                url = f"https://duckduckgo.com/?q={url.replace(' ', '+')}"
            current_browser.setUrl(QUrl(url))

    def update_url_bar(self, url, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(url.toString())

    def navigate_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def navigate_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def reload_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def go_home(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            homepage = QUrl("https://ambikeshishere.github.io/Landing-page/")
            current_browser.setUrl(homepage)

    def show_bookmarks(self):
        if self.bookmarks:
            bookmarks_html = "".join([f'<li><a href="{b}">{b}</a></li>' for b in self.bookmarks])
            html_content = f"<h1>Bookmarks</h1><ul>{bookmarks_html}</ul>"
            current_browser = self.tabs.currentWidget()
            if current_browser:
                current_browser.setHtml(html_content)
        else:
            current_browser = self.tabs.currentWidget()
            if current_browser:
                current_browser.setHtml("<h1>No bookmarks added</h1>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
