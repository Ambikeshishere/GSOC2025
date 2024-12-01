import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

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
        self.setWindowTitle("Python Browser")
        self.setGeometry(100, 100, 1024, 768)

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

    # def show_bookmarks(self):
    #     if self.bookmarks:
    #         bookmark_list = "\n".join(self.bookmarks)
    #         self.browser.setHtml(f"<h1>Bookmarks</h1><ul>{''.join(f'<li><a href="{b}">{b}</a></li>' for b in self.bookmarks)}</ul>")
    #     else:

    def show_bookmarks(self):
        if self.bookmarks:
            bookmarks_html = "".join([f'<li><a href="{b}">{b}</a></li>' for b in self.bookmarks])
            html_content = f"<h1>Bookmarks</h1><ul>{bookmarks_html}</ul>"
            self.browser.setHtml(html_content)
        else:
            self.browser.setHtml("<h1>No bookmarks added</h1>")



#Code Updated
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
