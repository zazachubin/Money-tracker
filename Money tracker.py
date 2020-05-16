##!/usr/bin/python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------- Libraries ---------------------------------------------------
from PyQt5.QtWidgets import QMainWindow, QApplication, QPlainTextEdit, QDateTimeEdit, QFileDialog, QTableWidget, QLineEdit, QSplitter, QHeaderView, QLabel, QHeaderView, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QLinearGradient, QColor, QBrush, QPalette
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDir
from Table import OutcomeTable, IncomeTable
from EventClasterTable import OutcomeEventClaster, IncomeEventClaster
from datetime import datetime
import json
import sys

class App(QMainWindow):
# +++++++++++++++++++++++++++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++++++++++++++++++++++
	def __init__(self):
		QMainWindow.__init__(self,None)
		self.outcomeTable_header = ['დრო','მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
		self.temp_data = { 	'config': { 'language' : 'georgian',
										'length'   : 1500, 
										'width'    : 900},
							'calendarRange' : { 'start_date' : '12.02.2018',
			  					 				'stop_date'  : '22.02.2020'},
							'outcomeTableData' : {},
							'incomeTableData'  : {}}
		self._filePath = ""
		self._tt = True
# -------------------------------------------------- Initialization ------------------------------------------------
		self.initUI()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++ initUI ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def initUI(self):
		QMainWindow.__init__(self)
		self.setWindowTitle('ფინანსების მართვა')
		self.setWindowIcon(QtGui.QIcon("icon/finance.png"))
		self.setGeometry(250, 100, int(self.temp_data['config']['length']), int(self.temp_data['config']['width']))
# ---------------------------------------------- set date on status ber --------------------------------------------
		now = datetime.now()
		self.statusBar().showMessage(now.strftime("%d-%m-%Y"))
# --------------------------------------------------- Create Menu --------------------------------------------------
		mainMenu = self.menuBar()
# ------------------------------------------------ Create tabs widget ----------------------------------------------
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tab3 = QWidget()
# ------------------------------------------------ create menu options ---------------------------------------------
		fileMenu = mainMenu.addMenu('ფაილი')
		editMenu = mainMenu.addMenu('რედაქტირება')
		viewMenu = mainMenu.addMenu('ინტერფეისი')
		toggleTool = QAction("ინსტრუმენტთა ველი 1",self,checkable=True)
		toggleTool.triggered.connect(self.handleToggleTool)

		viewMenu.addAction(toggleTool)
# ----------------------------------------------------- ToolBar ----------------------------------------------------
# -------------------------------------------------- Exit toolbar --------------------------------------------------
		exitAct = QAction(QIcon('icon/close.png'),'გასვლა', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.triggered.connect(app.quit)
# ------------------------------------------------------- new ------------------------------------------------------
		newAct = QAction(QIcon('icon/new.png'),'ახალი', self)
		newAct.setShortcut("Ctrl+N")
		newAct.triggered.connect(self.new)
# ------------------------------------------------------- open -----------------------------------------------------
		openAct = QAction(QIcon('icon/open.png'),'გახსნა', self)
		openAct.setShortcut("Ctrl+O")
		openAct.triggered.connect(self.openFile)
#-------------------------------------------------------- Save -----------------------------------------------------
# --------------------------------------------------- Save toolbar -------------------------------------------------
		saveAct = QAction(QIcon('icon/save.png'),'შენახვა', self)
		saveAct.setShortcut("Ctrl+S")
		saveAct.triggered.connect(lambda : self.save(self._filePath))
# ------------------------------------------------- Save as toolbar ------------------------------------------------
		save_asAct = QAction(QIcon('icon/save_as.png'), 'შენახვა როგორც', self)
		save_asAct.triggered.connect(self.saveAs)
# ---------------------------------------------------- Add Event ---------------------------------------------------
		addEventClasterAct = QAction(QIcon('icon/addEvent.svg'), 'დამატება', self)
		addEventClasterAct.triggered.connect(lambda : self.addOutcomeEventClaster() if self.tabs.currentIndex() == 0 else self.addIncomeEventClaster())
# --------------------------------------------------- Edit Event ---------------------------------------------------
		EditEventClasterAct = QAction(QIcon('icon/EditEvent.svg'), 'რედაქტირება', self)
		EditEventClasterAct.triggered.connect(lambda : self.editOutcomeEventClaster() if self.tabs.currentIndex() == 0 else self.editIncomeEventClaster())
# -------------------------------------------------- Remove Event --------------------------------------------------
		removeEventClasterAct = QAction(QIcon('icon/RemoveEvent.svg'), 'წაშლა', self)
		removeEventClasterAct.triggered.connect(lambda : self.removeOutcomeEventClaster() if self.tabs.currentIndex() == 0 else self.removeIncomeEventClaster())
# -------------------------------------------------- calendar range ------------------------------------------------
		CalendarAct = QAction(QIcon('icon/calendar.png'), 'კალენდარი', self)
		CalendarAct.triggered.connect(self.calendarRange)
		self.statusBarMessage('კალენდარი')
# ---------------------------------------------------- settings  ---------------------------------------------------
		settingsAct = QAction(QIcon('icon/settings.png'), 'პარამეტრები', self)
		settingsAct.triggered.connect(self.settings)
# ---------------------------------------------- Print data structure ----------------------------------------------
		printAct = QAction(QIcon('icon/print.png'), 'მონაცემთა დაბეჭვდა', self)
		printAct.triggered.connect(self.printData)
		printAct.triggered.connect(lambda : self.statusBarMessage('მონაცემთა დაბეჭვდა'))
# ------------------------------------------------------ Test ------------------------------------------------------
		testAct = QAction(QIcon('icon/test.png'), 'ტესტი', self)
		testAct.triggered.connect(self.test)
		testAct.triggered.connect(lambda : self.statusBarMessage('ტესტი'))
# ------------------------------------------- add buttons on first toolbar -----------------------------------------
		self.toolbar = self.addToolBar('Tools')
		self.toolbar.addAction(exitAct)
		self.toolbar.addSeparator()
		self.toolbar.addAction(newAct)
		self.toolbar.addAction(openAct)
		self.toolbar.addAction(saveAct)
		self.toolbar.addAction(save_asAct)
		self.toolbar.addSeparator()
		self.toolbar.addAction(addEventClasterAct)
		self.toolbar.addAction(EditEventClasterAct)
		self.toolbar.addAction(removeEventClasterAct)
		self.toolbar.addAction(testAct)
		self.toolbar.addAction(CalendarAct)
		self.toolbar.addSeparator()
		self.toolbar.addAction(settingsAct)

		self.addToolBarBreak()
		self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.addToolBar(Qt.TopToolBarArea , self.toolbar)
# ------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- add tab pages -------------------------------------------------
# ---------------------------------------------------- Add tabs ----------------------------------------------------
		self.tabs.addTab(self.tab1, "ხარჯები")
		self.tabs.addTab(self.tab2, "შემოსავალები")
		self.tabs.addTab(self.tab3, "ტერმინალი")
		self.setCentralWidget(self.tabs)
# ------------------------------------------------ set tab1 layouts ------------------------------------------------
		self.VlayoutTab1 = QVBoxLayout()
# ------------------------------------------------ set tab2 layouts ------------------------------------------------
		self.VlayoutTab2 = QVBoxLayout()
# ------------------------------------------------ set tab4 layouts ------------------------------------------------
		self.VlayoutTab3 = QVBoxLayout()
# -------------------------------------------------- Outcome Table -------------------------------------------------
		self.outcomeTable = OutcomeTable()
		self.VlayoutTab1.addWidget(self.outcomeTable)
# -------------------------------------------------- Income Table --------------------------------------------------
		self.incomeTable = IncomeTable()
		self.VlayoutTab2.addWidget(self.incomeTable)
#------------------------------------------------------ Terminal ---------------------------------------------------
		self.terminal = QPlainTextEdit(self)
		self.VlayoutTab3.addWidget(self.terminal)
		self.terminal.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(100,255,255,20); color: rgb(255,255,255);"
                                 "border-style: solid; border-radius: 8px; border-width: 3px; border-color: rgba(0,140,255,255);")
# ------------------------------------------------- set tab 1 layout  ----------------------------------------------
		self.tab1.setLayout(self.VlayoutTab1)
# ------------------------------------------------- set tab 2 layout  ----------------------------------------------
		self.tab2.setLayout(self.VlayoutTab2)
# ------------------------------------------------- set tab 4 layout  ----------------------------------------------
		self.tab3.setLayout(self.VlayoutTab3)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ new ++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def new(self):
		NewFilePath, _ = QFileDialog.getSaveFileName(self, 'ახალი ფაილი', QDir.homePath(), "JSON Files(*.json)")
		if len(NewFilePath) != 0:
			self._filePath = NewFilePath

			self.temp_data = {	'config': { 'language' : 'georgian',
											'length'   : 1500, 
											'width'    : 900},
								'calendarRange' : { 'start_date' : '12.02.2018',
			  					 					'stop_date'  : '22.02.2020'},
								'outcomeTableData' : {},
								'incomeTableData'  : {}}
			self.save(self._filePath)
			self.importData(self._filePath)
			if len(self.temp_data['outcomeTableData']) != 0:
				self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
				self.incomeTable.importEvents(self.temp_data['incomeTableData'])
			self.statusBarMessage('ახალი')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ open +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def openFile(self):
		self._filePath, _ = QFileDialog.getOpenFileName(self, 'ფაილის გახსნა', QDir.currentPath(), "JSON Files(*.json)")
		if len(self._filePath) != 0:
			self.importData(self._filePath)
			if len(self.temp_data['outcomeTableData']) != 0:
				self.temp_data['outcomeTableData'] = self.sortDateClasters(self.temp_data['outcomeTableData'])
				self.temp_data['incomeTableData'] = self.sortDateClasters(self.temp_data['incomeTableData'])
				self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
				self.incomeTable.importEvents(self.temp_data['incomeTableData'])
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ Save +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def save(self,Path):
		if Path != '':
			with open(Path, 'w') as outfile:
				json.dump(self.temp_data, outfile, indent=4)
			self.statusBarMessage('შენახვა')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++ Save as ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def saveAs(self):
		path, _ = QFileDialog.getSaveFileName(self, 'ფაილის შენახვა', QDir.homePath(), "JSON Files(*.json)")
		if len(path) != 0:
			self._filePath = path
			self.save(self._filePath)
			self.statusBarMessage('შენახვა როგორც')
# +++++++++++++++++++++++++++++++++++++++++++++++ Sort dateClasters ++++++++++++++++++++++++++++++++++++++++++++++++
	def sortDateClasters(self, dateClasters):
		datesArray = dateClasters.keys()
		timeArray = []
		for item in datesArray:
			timeArray.append(item)
		dates = [datetime.strptime(ts, "%d.%m.%Y") for ts in timeArray]
		dates.sort()
		sorteddates = [datetime.strftime(ts, "%d.%m.%Y") for ts in dates]
		sortedTimeStamps = {}
		for date in sorteddates:
			sortedTimeStamps.update({date : dateClasters[date]})
		return sortedTimeStamps
# ++++++++++++++++++++++++++++++++++++++++++++++++++++ importData ++++++++++++++++++++++++++++++++++++++++++++++++++
	def importData(self,filePath):
		self._filePath = filePath
		try:
			with open(self._filePath, 'r') as f:
				self.temp_data = json.load(f)
			self.statusBarMessage('მონაცემთა შემოტანა')
		except FileNotFoundError:
			self.statusBarMessage('ფაილი ვერ მოიძებნა')
			pass
		except UnicodeDecodeError:
			self.statusBarMessage('არასწორი ფორმატი')
			pass
# ++++++++++++++++++++++++++++++++++++++++++ Print data structure button +++++++++++++++++++++++++++++++++++++++++++
	def printData(self):
		self.term(" კონფიგურაცია ---> " + str(self.temp_data['config']))
		self.term(" კალენდარი start_date ---> " + str(self.temp_data['calendarRange']['start_date']))
		self.term(" კალენდარი stop_date ---> " + str(self.temp_data['calendarRange']['stop_date']))
		self.term(" ხარჯები ---> " + str(self.temp_data['outcomeTableData']))
		self.term(" შემოსავლები ---> " + str(self.temp_data['incomeTableData']))
		self.statusBarMessage("მონაცემთა დაბეჭვდა")
# +++++++++++++++++++++++++++++++++++++++++++++++++ Calendar range +++++++++++++++++++++++++++++++++++++++++++++++++
	def calendarRange(self):
		from CalendarDialog import CalendarDialog
		diag = CalendarDialog()
		diag.setCalendarRange(self.temp_data['calendarRange'])
		diag.exec_()
		dateRange, applayState = diag.getRange()
		if applayState == True:
			self.temp_data['calendarRange'] = dateRange
# +++++++++++++++++++++++++++++++++++++++++++++++++++++ settings +++++++++++++++++++++++++++++++++++++++++++++++++++
	def settings(self):
		from SettingsDialog import Settings
		dialog = Settings(self.temp_data['config'])
		dialog.exec_()
		self.setGeometry(250, 100, int(self.temp_data['config']["length"]), int(self.temp_data['config']["width"]))
		self.statusBarMessage("პარამეტრები")
# ++++++++++++++++++++++++++++++++++++++++++++ Add Outcome Event Claster +++++++++++++++++++++++++++++++++++++++++++
	def addOutcomeEventClaster(self):
		Outcomedialog = OutcomeEventClaster()
		Outcomedialog.exec_()
		DataClasterPart, applayState = Outcomedialog.getDataClasterPart()
		if applayState == True:
			self.temp_data['outcomeTableData'].update(DataClasterPart)
			self.temp_data['outcomeTableData'] = self.sortDateClasters(self.temp_data['outcomeTableData'])
			self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
# ++++++++++++++++++++++++++++++++++++++++++++ Add Income Event Claster ++++++++++++++++++++++++++++++++++++++++++++
	def addIncomeEventClaster(self):
		Incomedialog = IncomeEventClaster()
		Incomedialog.exec_()
		DataClasterPart, applayState = Incomedialog.getDataClasterPart()
		if applayState == True:
			self.temp_data['incomeTableData'].update(DataClasterPart)
			self.temp_data['incomeTableData'] = self.sortDateClasters(self.temp_data['incomeTableData'])
			self.incomeTable.importEvents(self.temp_data['incomeTableData'])
# +++++++++++++++++++++++++++++++++++++++++++ Edit Outcome Event Claster +++++++++++++++++++++++++++++++++++++++++++
	def editOutcomeEventClaster(self):
		row = self.outcomeTable.currentRow()
		column = self.outcomeTable.currentColumn()
		try:
			selectedDate = self.outcomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
			Outcomedialog = OutcomeEventClaster()
			Outcomedialog.EditDataClaster(self.temp_data['outcomeTableData'][selectedDate], selectedDate)
			Outcomedialog.exec_()
			DataClasterPart, applayState = Outcomedialog.getDataClasterPart()
			if applayState == True:
				if {selectedDate : self.temp_data['outcomeTableData'][selectedDate]}.keys() != DataClasterPart.keys():
					del self.temp_data['outcomeTableData'][selectedDate]
				self.temp_data['outcomeTableData'].update(DataClasterPart)
				self.temp_data['outcomeTableData'] = self.sortDateClasters(self.temp_data['outcomeTableData'])
				self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
		except AttributeError:
			pass
# +++++++++++++++++++++++++++++++++++++++++++ Edit Income Event Claster ++++++++++++++++++++++++++++++++++++++++++++
	def editIncomeEventClaster(self):
		row = self.incomeTable.currentRow()
		column = self.incomeTable.currentColumn()
		try:
			selectedDate = self.incomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
			Incomedialog = IncomeEventClaster()
			Incomedialog.EditDataClaster(self.temp_data['incomeTableData'][selectedDate], selectedDate)
			Incomedialog.exec_()
			DataClasterPart, applayState = Incomedialog.getDataClasterPart()
			if applayState == True:
				if {selectedDate : self.temp_data['incomeTableData'][selectedDate]}.keys() != DataClasterPart.keys():
					del self.temp_data['incomeTableData'][selectedDate]
				self.temp_data['incomeTableData'].update(DataClasterPart)
				self.temp_data['incomeTableData'] = self.sortDateClasters(self.temp_data['incomeTableData'])
				self.incomeTable.importEvents(self.temp_data['incomeTableData'])
		except AttributeError:
			pass
# ++++++++++++++++++++++++++++++++++++++++++ Remove Outcome Event Claster ++++++++++++++++++++++++++++++++++++++++++
	def removeOutcomeEventClaster(self):
		row = self.outcomeTable.currentRow()
		column = self.outcomeTable.currentColumn()
		if column == 0:
			selectedDate = self.outcomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
			del self.temp_data['outcomeTableData'][selectedDate]
			self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
# ++++++++++++++++++++++++++++++++++++++++++ Remove Income Event Claster +++++++++++++++++++++++++++++++++++++++++++
	def removeIncomeEventClaster(self):
		row = self.incomeTable.currentRow()
		column = self.incomeTable.currentColumn()
		if column == 0:
			selectedDate = self.incomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
			del self.temp_data['incomeTableData'][selectedDate]
			self.incomeTable.importEvents(self.temp_data['incomeTableData'])
# +++++++++++++++++++++++++++++++++++++++++++++++++ Terminal Print +++++++++++++++++++++++++++++++++++++++++++++++++
	def term(self, Text):
		self.terminal.insertPlainText("-----------------------------\n")
		self.terminal.insertPlainText("----> " + Text + "\n")
		self.terminal.insertPlainText("-----------------------------\n")
		self.statusBarMessage("ტერმინალში ბეჭვდა")
# ++++++++++++++++++++++++++++++++++++++++++++++++ StatusBar Message +++++++++++++++++++++++++++++++++++++++++++++++
	def statusBarMessage(self,message):
		self.statusBar().showMessage(message)
# ++++++++++++++++++++++++++++++++++++++++++++++++ Toolbar Hide-Show +++++++++++++++++++++++++++++++++++++++++++++++
	def handleToggleTool(self):
		if self._tt == True:
			self.toolbar.hide()
			self._tt = False
		else:
			self.toolbar.show()
			self._tt = True
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ Test +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def test(self):
		'''
		#self.addEventClaster()
		outcomeData =  {  '22.01.1993': [[ {'cell_0': 'პური'},
									{'cell_1.1': '2', 'cell_1.2': 1},
									{'cell_2.1': 2},
									{   'cell_3.1': '30',
										'cell_3.2': 1,
										'cell_3.3': '--',
										'cell_3.4': 0},
									{'cell_4': False}],
								  [ {'cell_0': 'ლობიო'},
									{'cell_1.1': '5', 'cell_1.2': 1},
									{'cell_2.1': 3},
									{   'cell_3.1': '64',
										'cell_3.2': 2,
										'cell_3.3': '--',
										'cell_3.4': 0},
									{'cell_4': False}]],
				   '23.01.1993': [[ {'cell_0': 'იოგურტი'},
									{'cell_1.1': '5', 'cell_1.2': 0},
									{'cell_2.1': 2},
									{   'cell_3.1': '30',
										'cell_3.2': 1,
										'cell_3.3': '100',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'ლობიო'},
									{'cell_1.1': '2', 'cell_1.2': 0},
									{'cell_2.1': 3},
									{   'cell_3.1': '44',
										'cell_3.2': 2,
										'cell_3.3': '--',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'წიწიბურა'},
									{'cell_1.1': '5', 'cell_1.2': 1},
									{'cell_2.1': 3},
									{   'cell_3.1': '64',
										'cell_3.2': 2,
										'cell_3.3': '54',
										'cell_3.4': 0},
									{'cell_4': True}]],
				   '24.01.1993': [[ {'cell_0': 'იოგურტი'},
									{'cell_1.1': '5', 'cell_1.2': 0},
									{'cell_2.1': 2},
									{   'cell_3.1': '30',
										'cell_3.2': 1,
										'cell_3.3': '100',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'სიმინდი'},
									{'cell_1.1': '2', 'cell_1.2': 0},
									{'cell_2.1': 3},
									{   'cell_3.1': '44',
										'cell_3.2': 2,
										'cell_3.3': '--',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'ბანანი'},
									{'cell_1.1': '2', 'cell_1.2': 0},
									{'cell_2.1': 3},
									{   'cell_3.1': '44',
										'cell_3.2': 2,
										'cell_3.3': '24',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'ვაშლი'},
									{'cell_1.1': '2', 'cell_1.2': 0},
									{'cell_2.1': 3},
									{   'cell_3.1': '44',
										'cell_3.2': 2,
										'cell_3.3': '24',
										'cell_3.4': 0},
									{'cell_4': True}]]}
		self.outcomeTable.importEvents(outcomeData)
		incomeData =  {   '22.01.1993': [[{'cell_0': 0},
									{'cell_1.1': '16500', 'cell_1.2': 0}],
								   [{'cell_0': 2},
									{'cell_1.1': '6000', 'cell_1.2': 0}]],
							'23.01.1993': [[{'cell_0': 0},
											{'cell_1.1': '16500', 'cell_1.2': 0}]],
							'24.01.1993': [[{'cell_0': 0},
											{'cell_1.1': '16500', 'cell_1.2': 0}],
										[{'cell_0': 2},
											{'cell_1.1': '6000', 'cell_1.2': 0}]]}
		self.incomeTable.importEvents(incomeData)
		EventEnterdialog = IncomeEventClaster()
		#EventEnterdialog = OutcomeEventClaster()
		EventEnterdialog.EditDataClaster(incomeData['24.01.1993'], '24.01.1993')
		#EventEnterdialog.EditDataClaster(outcomeData['24.01.1993'], '24.01.1993')
		EventEnterdialog.exec_()
		'''
		self.printData()
		self.statusBarMessage('ტესტი')
####################################################################################################################
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	app.setStyle('Fusion')
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53, 53, 53))
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, QColor(25, 25, 25))
	palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	palette.setColor(QPalette.ToolTipBase, Qt.white)
	palette.setColor(QPalette.ToolTipText, Qt.white)
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, QColor(53, 53, 53))
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Link, QColor(42, 130, 218))
	palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	palette.setColor(QPalette.HighlightedText, Qt.black)
	app.setPalette(palette)

	ex.show()
	sys.exit(app.exec_())