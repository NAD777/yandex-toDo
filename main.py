import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
import csv
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.inbox_btn.clicked.connect(self.open_inbox)
        self.today_btn.clicked.connect(self.open_today)
        self.plans_btn.clicked.connect(self.open_plans)
        self.logbook_btn.clicked.connect(self.open_logbook)
    
    def open_inbox(self):
        self.clear_highlights()
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232);")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Inbox())
        # self.content.setWidget(Example())

    def open_today(self):
        self.clear_highlights()
        self.today_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232);")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Today())
        # self.content.setWidget(Example())
    
    def open_plans(self):
        self.clear_highlights()
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232);")
    
    def open_logbook(self):
        self.clear_highlights()
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232);")
    
    def clear_highlights(self):
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251)")
        self.today_btn.setStyleSheet("padding:5px;border:none; background-color: rgb(249, 250, 251)")
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251)")
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251)")

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class Inbox(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('inbox_widget.ui', self)


class Today(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('today_widget.ui', self)


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())