from PyQt5.QtWidgets import (QApplication, QDialog, QCalendarWidget,
                             QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
import sys
# ~~~~~~~~~~~~~~~~~~~~~~~~ Calendar Dialog ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CalendarDialog(QDialog):
# ++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.applayState = False
        self.dateRange = {'calendarRange' : {'start_date' : '',
                                             'stop_date'  : ''}}
        self.vbox_general = QVBoxLayout()
        self.hbox_general = QHBoxLayout()
        self.hbox_buttons = QHBoxLayout()

        self.vbox_calendar1 = QVBoxLayout()
        self.vbox_calendar2 = QVBoxLayout()

        self.range_from = QLabel("from")
        self.range_to = QLabel("to")

        self.fromCalendar = QCalendarWidget(self)
        self.toCalendar = QCalendarWidget(self)

        self.setWindowTitle("კალენდარი")
        self.setWindowIcon(QtGui.QIcon("icon/calendar.svg"))
        self.vbox_calendar1.addWidget(self.range_from)
        self.vbox_calendar1.addWidget(self.fromCalendar)
        self.vbox_calendar2.addWidget(self.range_to)
        self.vbox_calendar2.addWidget(self.toCalendar)

        self.hbox_general.addLayout(self.vbox_calendar1)
        self.hbox_general.addLayout(self.vbox_calendar2)
# ----------------- Create apply and cancel buttons -------------------
        self.ApplySet = QPushButton("დასტური",self)
        self.CancelSet = QPushButton("გაუქმება",self)

        self.ApplySet.clicked.connect(self.applyCalendar)
        self.CancelSet.clicked.connect(self.CancelCalendar)
# ------------- Add apply and cancel buttons on layout ----------------
        self.hbox_buttons.addWidget(self.ApplySet)
        self.hbox_buttons.addWidget(self.CancelSet)
# -------------------------- Set Layouts ------------------------------
        self.vbox_general.addLayout(self.hbox_general)
        self.vbox_general.addLayout(self.hbox_buttons)
        self.setLayout(self.vbox_general)
        self.show()
# -------------------------- Set calendar -----------------------------
    def setCalendarRange(self, dateRange):
        self.dateRange = dateRange
        self.fromCalendar.setSelectedDate(QDate(QDate.fromString(self.dateRange['start_date'], 'dd.MM.yyyy').getDate()[0], 
                                        QDate.fromString(self.dateRange['start_date'], 'dd.MM.yyyy').getDate()[1], 
                                        QDate.fromString(self.dateRange['start_date'], 'dd.MM.yyyy').getDate()[2]))
        self.toCalendar.setSelectedDate(QDate(QDate.fromString(self.dateRange['stop_date'], 'dd.MM.yyyy').getDate()[0],
                                        QDate.fromString(self.dateRange['stop_date'], 'dd.MM.yyyy').getDate()[1], 
                                        QDate.fromString(self.dateRange['stop_date'], 'dd.MM.yyyy').getDate()[2]))
# +++++++++++++++++++++++++++ get Range +++++++++++++++++++++++++++++++
    def getRange(self):
        return self.dateRange, self.applayState
# ++++++++++++++++++++++++ Apply calendar +++++++++++++++++++++++++++++
    def applyCalendar(self):
        self.dateRange['start_date'] = self.fromCalendar.selectedDate().toString("dd.MM.yyyy")
        self.dateRange['stop_date'] = self.toCalendar.selectedDate().toString("dd.MM.yyyy")
        self.applayState = True
        self.close()
# ++++++++++++++++++++++++ Cancel calendar ++++++++++++++++++++++++++++
    def CancelCalendar(self):
        self.applayState = False
        self.close()

if __name__ == '__main__':
    calendarRange = {'start_date' : '12.02.2018',
                      'stop_date'  : '22.02.2020'}
    app = QApplication(sys.argv)
    diag = CalendarDialog()
    diag.setCalendarRange(calendarRange)
    app.exec_()