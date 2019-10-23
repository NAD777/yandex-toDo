import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton
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
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Part())
    
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
        self.add_btn.clicked.connect(self.add_part)
    
    def add_part(self):
        self.verticalLayout.addWidget(Part())


class Today(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('today_widget.ui', self)


class Part(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('part.ui', self)
    
    def mousePressEvent(self, event):
        print('1 click')
        if event.button() == Qt.LeftButton:
            self.setStyleSheet("background-color: rgb(213, 224, 252)")
    
    def mouseDoubleClickEvent(self, event):   
        print('2 click!')
        self.verticalLayout.addWidget(QPushButton())
    

app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())