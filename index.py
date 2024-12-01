import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, ad_domains):
        super().__init__()
        self.ad_domains = ad_domains

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        for domain in self.ad_domains:
            if domain in url:
                print(f"Blocked: {url}")  # For debugging purposes
                info.block(True)
                return

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ad_domains = self.load_ad_domains()

        # Create a web engine profile and set the ad blocker
        profile = QWebEngineProfile.defaultProfile()
        ad_blocker = AdBlocker(self.ad_domains)
        profile.setRequestInterceptor(ad_blocker)

        # Set up the browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Navigation buttons
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.browser.back)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.browser.forward)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.browser.reload)

        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_home)

        self.bookmark_button = QPushButton("Bookmark")
        self.bookmark_button.clicked.connect(self.add_bookmark)

        self.bookmarks = []
        self.bookmarks_button = QPushButton("Show Bookmarks")
        self.bookmarks_button.clicked.connect(self.show_bookmarks)

        # Layout setup
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.next_button)
        top_layout.addWidget(self.refresh_button)
        top_layout.addWidget(self.home_button)
        top_layout.addWidget(self.bookmark_button)
        top_layout.addWidget(self.bookmarks_button)
        top_layout.addWidget(self.url_bar)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addLayout(top_layout)
        layout.addWidget(self.browser)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Python Browser with AdBlocker")
        self.setGeometry(100, 100, 1024, 768)

    def load_ad_domains(self):
        # Example list of ad-serving domains
        # Ideally, this would be loaded from a file or online source
        return [
            "doubleclick.net",
            "adservice.google.com",
            "googlesyndication.com",
            "ads.pubmatic.com",
            "amazon-adsystem.com",
            "adroll.com",
            "taboola.com"
        ]

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)

    def show_bookmarks(self):
        if self.bookmarks:
            bookmark_list = "\n".join(self.bookmarks)
            self.browser.setHtml(f"<h1>Bookmarks</h1><ul>{''.join(f'<li><a href="{b}">{b}</a></li>' for b in self.bookmarks)}</ul>")
        else:
            self.browser.setHtml("<h1>No bookmarks added</h1>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
