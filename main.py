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
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251);")
        self.today_btn.setStyleSheet("padding:5px;border:none; background-color: rgb(249, 250, 251);")
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251);")
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251);")

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
        self.refresh_btn.clicked.connect(self.refresh)
        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.refresh()
        
    def refresh(self):
        res = self.cur.execute("""SELECT * FROM Inbox""")
        for el in res:
            self.scrollLayout.addRow(Part(el[0], el[1], el[2]))
    
    def remove_done(self):
        for i in range(self.scrollLayout.rowCount()):
            if self.scrollLayout.itemAt(i).widget().is_checked():
                pass
    
    def mousePressEvent(self, event):
        for i in range(self.scrollLayout.rowCount()):
            self.scrollLayout.itemAt(i).widget().hide_adds()
        print('inbox field clicked')
    
    def add_part(self):
        part = Part()
        self.scrollLayout.addRow(part)
        part.text_edit_clicked()


class Today(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('today_widget.ui', self)


class Part(QWidget):
    def __init__(self, id=None, text=None, desr=None):
        super().__init__()
        self.id = id
        self.text = text
        self.desr = desr

        uic.loadUi('part.ui', self)
        self.lineEdit = cQLineEdit(self)
        self.lineEdit.setStyleSheet("padding:5px;")
        self.lineEdit.clicked.connect(self.text_edit_clicked)

        self.gridLayout.addWidget(self.lineEdit, 0, 1)
        self.setLayout(self.gridLayout)
        self.lineEdit.setReadOnly(True)
        self.textEdit.hide()

        if self.text is not None:
            self.lineEdit.setText(self.text)
        
        if self.desr is not None:
            self.textEdit.setText(self.desr)

    def is_checked(self):
        if self.checkBox == Qt.Checked:
            return True
        return False

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
        self.setPlaceholderText('Новая задача')
    
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())