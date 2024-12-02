import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QHBoxLayout, QTabWidget, QCheckBox, QDialog, QFormLayout
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
        self.dark_mode = True  # Default mode is dark
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

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Search or enter a URL")
        self.update_url_bar_style()

        # Toolbar Buttons
        self.back_button = self.create_toolbar_button("⬅", "Back", self.navigate_back)
        self.forward_button = self.create_toolbar_button("➡", "Forward", self.navigate_forward)
        self.refresh_button = self.create_toolbar_button("⟳", "Refresh", self.reload_page)
        self.home_button = self.create_toolbar_button("🏠", "Home", self.go_home)
        self.bookmarks_button = self.create_toolbar_button("★", "Bookmarks", self.show_bookmarks)
        self.add_to_bookmarks_button = self.create_toolbar_button("☆", "Add to Bookmarks", self.add_to_bookmarks)
        self.new_tab_button = self.create_toolbar_button("➕", "New Tab", lambda: self.add_new_tab())
        self.settings_button = self.create_toolbar_button("⚙", "Settings", self.open_settings)

        # Toolbar Layout
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        toolbar_layout.addWidget(self.back_button)
        toolbar_layout.addWidget(self.forward_button)
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addWidget(self.home_button)
        toolbar_layout.addWidget(self.bookmarks_button)
        toolbar_layout.addWidget(self.add_to_bookmarks_button)
        toolbar_layout.addWidget(self.url_bar)
        toolbar_layout.addWidget(self.new_tab_button)
        toolbar_layout.addWidget(self.settings_button)

        toolbar = QWidget()
        toolbar.setLayout(toolbar_layout)
        self.update_toolbar_style(toolbar)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Window Properties
        self.update_window_style()
        self.setWindowTitle("Stark Browser")
        self.setWindowIcon(QIcon("icon.png"))  # Replace with your custom icon
        self.setGeometry(100, 100, 1024, 768)

    def create_toolbar_button(self, text, tooltip, callback):
        button = QPushButton(text)
        button.setToolTip(tooltip)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#3498db' if self.dark_mode else '#2980b9'};  /* Blue color */
                border: none;
                border-radius: 20px;  /* Circular shape */
                color: #FFFFFF;
                font-size: 14px;
                width: 30px;  /* Smaller size */
                height: 30px;  /* Smaller size */
                padding: 6px;
                text-align: center;
                line-height: 16px;
            }}
            QPushButton:hover {{
                background-color: {'#2980b9' if self.dark_mode else '#1c6ea4'};  /* Hover effect */
            }}
            QPushButton:pressed {{
                background-color: {'#1c6ea4' if self.dark_mode else '#1f4d7f'};  /* Pressed effect */
            }}
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

    def add_to_bookmarks(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            url = current_browser.url().toString()
            if url not in self.bookmarks:
                self.bookmarks.append(url)
                print(f"Added to bookmarks: {url}")

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

    def open_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        layout = QFormLayout()

        # Permissions
        location_checkbox = QCheckBox("Allow Location")
        camera_checkbox = QCheckBox("Allow Camera")
        microphone_checkbox = QCheckBox("Allow Microphone")

        layout.addRow(location_checkbox)
        layout.addRow(camera_checkbox)
        layout.addRow(microphone_checkbox)

        # Dark/Light Mode Toggle
        theme_checkbox = QCheckBox("Enable Dark Mode")
        theme_checkbox.setChecked(self.dark_mode)
        theme_checkbox.stateChanged.connect(lambda: self.toggle_theme(theme_checkbox.isChecked()))
        layout.addRow(theme_checkbox)

        dialog.setLayout(layout)
        dialog.exec()

    def toggle_theme(self, dark_mode):
        self.dark_mode = dark_mode
        self.update_window_style()

    def update_window_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {'#121212' if self.dark_mode else '#FFFFFF'}; }}
            QTabWidget::pane {{ border: 1px solid #444; border-radius: 12px; }}
            QTabBar::tab {{
                background: {'#1E1E1E' if self.dark_mode else '#F0F0F0'};
                color: {'#E0E0E0' if self.dark_mode else '#333'};
                padding: 8px 16px;
                border: 1px solid {'#444' if self.dark_mode else '#DDD'};
            }}
            QTabBar::tab:selected {{
                background: {'#4CAF50' if self.dark_mode else '#D9F5E3'};
                color: #FFFFFF;
            }}
        """)
        self.update_url_bar_style()

    def update_url_bar_style(self):
        self.url_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {'#1E1E1E' if self.dark_mode else '#F5F5F5'};
                color: {'#E0E0E0' if self.dark_mode else '#000000'};
                padding: 5px;
                border: 1px solid {'#4CAF50' if self.dark_mode else '#CCC'};
                border-radius: 10px;
            }}
        """)

    def update_toolbar_style(self, toolbar):
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {'#333' if self.dark_mode else '#F5F5F5'};
                border: 1px solid {'#444' if self.dark_mode else '#CCC'};
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
