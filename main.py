import sys
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton, QFormLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QInputDialog, QMessageBox
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
        self.open_inbox()
    
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
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Done())
    
    def clear_highlights(self):
        self.inbox_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251); border-radius: 8px;")
        self.today_btn.setStyleSheet("padding:5px;border:none; background-color: rgb(249, 250, 251); border-radius: 8px;")
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251); border-radius: 8px;")
        self.logbook_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(249, 250, 251); border-radius: 8px;")

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
        
        self.set_self_types(1)

        self.refresh()
    
    def set_self_types(self, type):
        self.types_of_parts = type

    def refresh(self):
        while self.scrollLayout.itemAt(0) is not None:
            self.scrollLayout.itemAt(0).widget().update()
            self.scrollLayout.removeRow(0)
        res = self.cur.execute(f"""SELECT * FROM Inbox WHERE type = '{self.types_of_parts}'""")
        for el in res:
            self.scrollLayout.addRow(Part(el[0], el[1], el[2], el[3]))
    
    def mousePressEvent(self, event):
        self.refresh()
        print('inbox field clicked')
    
    def add_part(self):
        part = Part()
        self.scrollLayout.addRow(part)
        part.text_edit_clicked()


class Today(QWidget):
    def __init__(self, *args):
        super().__init__()

class Done(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('inbox_widget.ui', self)
        self.add_btn.deleteLater()
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
        
        self.set_self_types(4)

        self.refresh()
    
    def set_self_types(self, type):
        self.types_of_parts = type

    def refresh(self):
        while self.scrollLayout.itemAt(0) is not None:
            self.scrollLayout.itemAt(0).widget().update()
            self.scrollLayout.removeRow(0)
        res = self.cur.execute(f"""SELECT * FROM Inbox WHERE type = '{self.types_of_parts}'""")
        for el in res:
            self.scrollLayout.addRow(Part(el[0], el[1], el[2], el[3]))
    
    def mousePressEvent(self, event):
        self.refresh()
        print('inbox field clicked')
    
    def add_part(self):
        part = Part()
        self.scrollLayout.addRow(part)
        part.text_edit_clicked()
        

class Part(QWidget):
    def __init__(self, id=None, text=None, desr=None, type=None):
        super().__init__()
        self.id = id
        self.text = text
        self.desr = desr
        self.type = type
        if self.type is None:
            self.type = 1
        self.type_changed = False

        uic.loadUi('part.ui', self)
        self.lineEdit = cQLineEdit(self)
        self.lineEdit.setStyleSheet("padding:5px;")
        self.lineEdit.clicked.connect(self.text_edit_clicked)

        self.gridLayout.addWidget(self.lineEdit, 0, 1)
        self.setLayout(self.gridLayout)
        self.lineEdit.setReadOnly(True)
        self.textEdit.hide()
        
        self.delete_btn.hide()
        self.delete_btn.clicked.connect(self.delete)

        if self.text is not None:
            self.text = str(self.text)
            self.lineEdit.setText(self.text)
        
        if self.desr is not None:
            self.desr = str(self.desr)
            self.textEdit.setText(self.desr)

        self.checkBox.stateChanged.connect(self.to_done)

        self.will_delete = False

        self.is_showing = True

    def to_done(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_out)
        self.timer.start(2000)

    def time_out(self):
        if self.checkBox.isChecked():
            self.is_showing = False
            self.type = 4
            self.type_changed = True
            self.update()
            self.type_changed = False
            print("Part hidden")
            self.hide()

    def delete(self):
        reply = QMessageBox.question(self, '', "Удалить?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            self.will_delete = True
            
    def update(self):
        if self.will_delete:
            self.con = sqlite3.connect('database.db')
            self.cur = self.con.cursor()
            self.cur.execute(f"""DELETE FROM Inbox WHERE id = '{self.id}'""")
            self.con.commit()
        
        elif self.text != self.lineEdit.text() or self.desr != self.textEdit.toPlainText() or self.type_changed:
            if self.id is not None and not self.will_delete:
                self.con = sqlite3.connect('database.db')
                self.cur = self.con.cursor()
                self.cur.execute(f"""UPDATE Inbox SET text = '{self.lineEdit.text()}', description = '{self.textEdit.toPlainText()}', type = '{self.type}' WHERE id = '{self.id}'""")
                self.con.commit()
            else:
                self.con = sqlite3.connect('database.db')
                self.cur = self.con.cursor()
                self.lineEdit_text = self.lineEdit.text()
                self.textEdit_text = self.textEdit.toPlainText()
                self.cur.execute(f"""INSERT INTO Inbox(text, description, type) VALUES('{self.lineEdit_text}', '{self.textEdit_text}', '{self.type}')""")
                self.con.commit()

    def is_checked(self):
        if self.checkBox == Qt.Checked:
            return True
        return False

    def text_edit_clicked(self):
        if self.is_showing: 
            self.textEdit.show()
            self.delete_btn.show()
            self.lineEdit.setReadOnly(False)
            self.lineEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")
            self.textEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")

    def hide_adds(self):
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet("background-color: rgb(249, 250, 251); padding:5px;border-radius: 8px;")
        self.textEdit.hide()
        self.delete_btn.hide()

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
        print(self.text())
        self.clicked.emit()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())