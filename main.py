import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton, QFormLayout, QVBoxLayout, QLineEdit
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
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Inbox())
        # self.content.setWidget(Example())

    def open_today(self):
        self.clear_highlights()
        self.today_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Today())
        # self.content.setWidget(Example())
    
    def open_plans(self):
        self.clear_highlights()
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Part())
    
    def open_logbook(self):
        self.clear_highlights()
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
    
    def clear_highlights(self):
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(239, 240, 241);")
        self.today_btn.setStyleSheet("padding:5px;border:none; background-color: rgb(239, 240, 241);")
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(239, 240, 241);")
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(239, 240, 241);")

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
        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

    def mousePressEvent(self, event):
        for i in range(self.scrollLayout.rowCount()):
            self.scrollLayout.itemAt(i).hide_adds()
        print('inbox field clicked')
    
    def add_part(self):
        self.scrollLayout.addRow(Part())


class Today(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('today_widget.ui', self)


class Part(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('part.ui', self)
        self.lineEdit = cQLineEdit(self)
        self.lineEdit.setText('123123')
        self.lineEdit.setStyleSheet("padding:5px;")
        self.lineEdit.clicked.connect(self.text_edit_clicked)

        self.gridLayout.addWidget(self.lineEdit, 0, 1)
        self.setLayout(self.gridLayout)
        self.lineEdit.setReadOnly(True)
        self.textEdit.hide()
        
        self.pushButton.clicked.connect(self.hide_adds)

    def text_edit_clicked(self):
        self.textEdit.show()
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")
        self.textEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")

    def hide_adds(self):
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet("background-color: rgb(249, 250, 251); padding:5px;border-radius: 8px;")
        self.textEdit.hide()

    def mousePressEvent(self, event):
        print('1 click')
    
    def mouseDoubleClickEvent(self, event):   
        print('2 click!')
        self.textEdit.show()
        self.lineEdit.setReadOnly(False)
        self.gridLayout.addWidget(QPushButton())


class cQLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, widget):
        super().__init__(widget)
    
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())