import platform
import socket
import sys
import threading
from PyQt4 import QtGui
from PyQt4.QtCore import QUrl, QSize, Qt
from PyQt4.QtGui import QMenuBar, QIcon, QApplication, QAction, QMainWindow, QWidget
from PyQt4.QtWebKit import QWebView
import webapp


class Application(QApplication):
    def __init__(self):
        if platform.system() == 'Linux':
            self.setAttribute(Qt.AA_X11InitThreads, True)
        QApplication.__init__(self, sys.argv)

        app_icon = QIcon()

        app_icon.addFile('./static/icon.iconset/icon_16x16.png', QSize(16, 16))
        app_icon.addFile('./static/icon.iconset/icon_32x32.png', QSize(32, 32))
        app_icon.addFile('./static/icon.iconset/icon_32x32@2x.png', QSize(64, 64))
        app_icon.addFile('./static/icon.iconset/icon_128x128.png', QSize(128, 128))
        app_icon.addFile('./static/icon.iconset/icon_256x256.png', QSize(256, 256))
        app_icon.addFile('./static/icon.iconset/icon_512x512.png', QSize(512, 512))

        self.setWindowIcon(app_icon)


class MainWindow(QMainWindow):
    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.port = port

        self.init_ui()

    def init_ui(self):
        self.resize(1100, 680)

        self.centralwidget = QWidget(self)

        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(0)

        self.html = QWebView()
        self.mainLayout.addWidget(self.html)
        self.setCentralWidget(self.centralwidget)

        self.html.load(QUrl("http://127.0.0.1:{0}".format(self.port)))

        # close_action = QAction('&Quit', self)
        # close_action.setShortcut('Cmd+Q')
        # close_action.setStatusTip('Quit Application')
        # close_action.triggered.connect(QtGui.qApp.quit)
        #
        # self.menubar = self.menuBar()
        # self.menubar.setNativeMenuBar(False)
        # file_menu = self.menubar.addMenu('&File')
        # file_menu.addAction(close_action)

        self.html.show()
        self.html.raise_()

        self.setWindowTitle('NeutronUI')

    def processtrigger(self, q):
        print(q.text() + ' is triggered')


def choose_port():
    temp_socket = socket.socket()
    temp_socket.bind(("127.0.0.1", 0))
    port = temp_socket.getsockname()[1]
    temp_socket.close()
    return port


def launch_window(port):
    app = Application()

    window = MainWindow(port)

    window.show()
    window.raise_()
    sys.exit(app.exec_())


def launch():
    port = choose_port()

    t = threading.Thread(target=webapp.app.run, kwargs={'port': port})
    t.daemon = True
    t.start()

    launch_window(port)


if __name__ == "__main__":
    launch()
