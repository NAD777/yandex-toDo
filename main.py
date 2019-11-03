import sys
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QDate
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton, QFormLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QInputDialog, QMessageBox
import csv
import sqlite3
from time import strftime, gmtime


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

    def open_today(self):
        self.clear_highlights()
        self.today_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Today())
    
    def open_plans(self):
        self.clear_highlights()
        self.plans_btn.setStyleSheet("padding:5px; border:none; background-color: rgb(225, 227, 232); border-radius: 8px;")
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(Plans())
    
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


class ListWidget(QWidget):
    def __init__(self, database_type_of_parts=None):
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
        
        self.set_self_types(database_type_of_parts)

    def set_self_types(self, type):
        self.types_of_parts = type

    def get_today_date(self):
        return strftime("%Y-%m-%d", gmtime())

    def get_type(self):
        return self.types_of_parts
        
    def refresh(self):
        # function for refresh scrollWidget 
        pass
    
    def clean_list(self):
        while self.scrollLayout.itemAt(0) is not None:
            self.scrollLayout.itemAt(0).widget().update()
            self.scrollLayout.removeRow(0)
    
    def get_res(self, type):
        return self.cur.execute(f"""SELECT * FROM Inbox WHERE type = '{self.get_type()}'""")

    def mousePressEvent(self, event):
        self.refresh()
        print('inbox field clicked')
    
    def add_part(self):
        part = Part()
        self.scrollLayout.addRow(part)
        part.text_edit_clicked()
    

class Inbox(ListWidget):
    def __init__(self, *args):
        super().__init__(1)
        self.move_to_inbox_what_was_missed()
        self.refresh()
    
    def move_to_inbox_what_was_missed(self):
        cur = self.get_today_date()
        res = self.cur.execute(f"""SELECT id FROM Inbox WHERE date < '{cur}' AND type = '3'""").fetchall()
        print(res)
        for _id in res:
            self.cur.execute(f"""UPDATE Inbox SET type = '1', date = 'None' WHERE id = '{_id[0]}'""")
        self.con.commit()

    def refresh(self):
        self.clean_list()
        res = self.get_res(self.get_type())
        for el in res:
            part = Part(id=el[0], text=el[1], desr=el[2], type=el[3], date=el[4])
            part.clear_date_btn.clicked.connect(self.refresh)
            self.scrollLayout.addRow(part)


class Today(ListWidget):
    def __init__(self, *args):
        super().__init__(3)
        self.refresh()

    def get_res(self, type):
        print(self.get_today_date())
        return self.cur.execute(f"""SELECT * FROM Inbox WHERE type = '{self.get_type()}' AND date = '{self.get_today_date()}'""")

    def refresh(self):
        self.clean_list()
        res = self.get_res(self.get_type())
        for el in res:
            part = Part(id=el[0], text=el[1], desr=el[2], type=el[3], date=el[4])
            part.clear_date_btn.clicked.connect(self.refresh)
            self.scrollLayout.addRow(part)
    
    def add_part(self):
        part = Part(type=3, date=self.get_today_date())
        part.something_changed = True
        part.clear_date_btn.clicked.connect(self.refresh)
        self.scrollLayout.addRow(part)
        part.text_edit_clicked()
        

class Plans(ListWidget):
    def __init__(self, *args):
        super().__init__(3)
        self.refresh()
        
    def get_res(self, begin, type):
        return self.cur.execute(f"""SELECT * FROM Inbox WHERE type = '{type}' AND date >= '{begin}'""").fetchall()

    def refresh(self):
        print("refresh")
        self.clean_list()
        res = sorted(self.get_res(self.get_today_date(), self.get_type()), key=lambda x: x[4])
        self.num_month_name = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
        prev_date = None
        for el in res:
            date_of_el = el[4]
            if prev_date != date_of_el:
                year, mon, day = date_of_el.split('-')
                mon = int(mon) - 1
                mon_name = self.num_month_name[mon]
                beautiful_date = f"<b>{day}</b> {mon_name} {year}"
                self.scrollLayout.addRow(Plans_part(beautiful_date))
            
            part = Part(id=el[0], text=el[1], desr=el[2], type=el[3], date=el[4])

            part.clear_date_btn.clicked.connect(self.refresh)
            part.set_date_btn.clicked.connect(self.refresh)

            self.scrollLayout.addRow(Part(id=el[0], text=el[1], desr=el[2], type=el[3], date=el[4]))
            prev_date = date_of_el

    def add_part(self):
        part = Part(type=self.get_type(), date=self.get_today_date())
        part.update()
        self.refresh()
        part.text_edit_clicked()


class Plans_part(QWidget):
    def __init__(self, text):
        super().__init__()
        uic.loadUi('part_plans.ui', self)
        self.label.setText(text)
        self.setLayout(self.verticalLayout_2)


class Done(ListWidget):
    def __init__(self, *args):
        super().__init__(4)
        self.add_btn.deleteLater()
        self.refresh()
    
    def refresh(self):
        self.clean_list()
        res = self.get_res(self.get_type())
        for el in res:
            self.scrollLayout.addRow(Part(id=el[0], text=el[1], desr=el[2], type=el[3], date=el[4]))


class Part(QWidget):
    def __init__(self, id=None, text=None, desr=None, type=None, date=None):
        super().__init__()
        uic.loadUi('part.ui', self)
        self.id = id
        self.text = text
        self.desr = desr
        self.type = type
        self.date = date
        if self.date == 'None':
            self.date = None
        if self.type is None:
            self.type = 1
        elif self.type == 4:
            self.checkBox.toggle()

        self.something_changed = False
        
        self.lineEdit = cQLineEdit(self)
        self.lineEdit.setStyleSheet("padding:5px;")
        self.lineEdit.clicked.connect(self.text_edit_clicked)

        self.calendarWidget.hide()

        self.gridLayout.addWidget(self.lineEdit, 0, 1)
        self.setLayout(self.gridLayout)
        self.lineEdit.setReadOnly(True)

        self.delete_btn.clicked.connect(self.delete)
        self.calendar_btn.clicked.connect(self.show_calendar)

        self.set_date_btn.clicked.connect(self.set_date)
        self.clear_date_btn.clicked.connect(self.clear_date)

        if self.text is not None:
            self.text = str(self.text)
            self.lineEdit.setText(self.text)
        
        if self.desr is not None:
            self.desr = str(self.desr)
            self.textEdit.setText(self.desr)

        self.checkBox.stateChanged.connect(self.to_done)

        self.will_delete = False

        self.is_showing = True

        self.calendar_is_showing = False

        self.hide_adds() 
    
    def get_today_date(self):
        return strftime("%Y-%m-%d", gmtime())

    def show_calendar(self):
        if self.calendar_is_showing:
            self.calendarWidget.hide()
            self.set_date_btn.hide()
            self.clear_date_btn.hide()
            self.calendar_is_showing = False
        else:
            self.calendarWidget.setMinimumDate(QDate(*map(int, self.get_today_date().split('-'))))
            if self.date is not None:
                self.calendarWidget.setSelectedDate(QDate(*map(int, self.date.split('-'))))
            else:
                self.calendarWidget.setSelectedDate(QDate(*map(int, self.get_today_date().split('-'))))
            self.calendarWidget.show()
            self.set_date_btn.show()
            self.clear_date_btn.show()
            self.calendar_is_showing = True

    def set_date(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if selected_date != self.date:
            print(selected_date, 1)
            self.something_changed = True
            if self.type != 4:
                self.hide()
                self.type = 3
            else:
                self.show_calendar()
            self.date = selected_date
            self.update()
    
    def clear_date(self):
        if self.type != 4:
            self.type = 1
        self.date = None
        self.something_changed = True
        self.show_calendar()
        self.update()

    def to_done(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_out)
        self.timer.start(2000)

    def time_out(self):
        if self.checkBox.isChecked():
            self.is_showing = False
            self.type = 4
            self.something_changed = True
            self.update()
            self.something_changed = False
            print("Part hidden")
            self.hide()
        elif self.type == 4:
            self.is_showing = False
            if self.date is None:
                self.type = 1
            else:
                today = self.get_today_date()
                if self.date < today:
                    self.date = None
                    self.type = 1
                else:
                    self.type = 3
            self.something_changed = True
            self.update()
            self.something_changed = False
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
        
        elif self.text != self.lineEdit.text() or self.desr != self.textEdit.toPlainText() or self.something_changed:
            if self.id is not None and not self.will_delete:
                self.con = sqlite3.connect('database.db')
                self.cur = self.con.cursor()
                self.cur.execute(f"""UPDATE Inbox SET text = '{self.lineEdit.text()}', description = '{self.textEdit.toPlainText()}', type = '{self.type}', date = '{self.date}' WHERE id = '{self.id}'""")
                self.con.commit()
            else:
                self.con = sqlite3.connect('database.db')
                self.cur = self.con.cursor()
                self.lineEdit_text = self.lineEdit.text()
                self.textEdit_text = self.textEdit.toPlainText()
                self.cur.execute(f"""INSERT INTO Inbox(text, description, type, date) VALUES('{self.lineEdit_text}', '{self.textEdit_text}', '{self.type}', '{self.date}')""")
                self.con.commit()

    def is_checked(self):
        if self.checkBox == Qt.Checked:
            return True
        return False

    def text_edit_clicked(self):
        if self.is_showing: 
            self.textEdit.show()
            self.delete_btn.show()
            self.calendar_btn.show()
            self.lineEdit.setReadOnly(False)
            self.lineEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")
            self.textEdit.setStyleSheet("background-color: rgb(213, 224, 252); padding:5px;border-radius: 8px;")

    def hide_adds(self):
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet("background-color: rgb(249, 250, 251); padding:5px;border-radius: 8px;")
        self.textEdit.hide()
        self.calendar_btn.hide()
        self.calendarWidget.hide()
        self.set_date_btn.hide()
        self.clear_date_btn.hide()
        self.delete_btn.hide()

    def mousePressEvent(self, event):
        print('1 click')
    
    def mouseDoubleClickEvent(self, event):   
        print('2 click!')


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