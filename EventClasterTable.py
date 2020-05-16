from PyQt5.QtWidgets import (	QApplication, QHeaderView, QDialog, QWidget, QLineEdit, QStyledItemDelegate, 
								QPushButton, QPlainTextEdit, QComboBox, QPlainTextEdit, QCheckBox, QCompleter, 
								QCalendarWidget, QHBoxLayout, QVBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDate
from pprint import pprint, pformat
import random
import sys

class TableItemCompleter(QStyledItemDelegate):
	def createEditor(self, parent, option, index):
		editor = QLineEdit(parent)
		completion_ls = index.data(Qt.UserRole)
		completer = QCompleter(completion_ls, parent)
		editor.setCompleter(completer)
		return editor
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Enter Info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OutcomeEventClaster(QDialog):
	def __init__(self, parent = None):
		QDialog.__init__(self, parent)
		self.applayState = False
		self.dataContainer = {}
		self._header = ['მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
		self._Currency = {	'₽'  : 'icon/Ruble.png',
							'$'  : 'icon/Dollar.png',
							'€'  : 'icon/Euro.png',
							'CHF': 'icon/swiss-franc.png',
							'₾'  : 'icon/Lari.png',
							'¥'  : 'icon/yuan.png'}
		self._units = ['--','ც','კგ','გრ','ლ','მლ','კვტ','თვე','დღე']
		self._category = [	'კვება','სხვადასხვა','ქირა','საყოფაცხოვრებო','კომუნალური','ტელეფონი',
							'ინტერნეტი','გართობა','ტანსაცმელი','ჰიგიენა','მედიკამენტები','ინტერნეტი',
							'ტრანსპორტი','მოწყობილობები','დასვენება','საჩუქარი','გამოწერა','საკომისიო','აღჭურვილობა',
							'ვარჯიში','რემონტი','ექიმთან კონსულტაცია','მკურნალობა','ჯარიმა','მოგზაურობა','გასესხება','გასესხებულის დაბრუნება','სესხი','სესხის დაბრუნება']
		self._EventNames = ["პური", "იოგურტი", "ლობიო", "შაქარი", "კარტოფილი"]
		self.date = [1993,1,22]
		
		self.InitUI()
		self.addRowWidgets()
		self.show()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ InitUI +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def InitUI(self):
		self.setWindowTitle("მონაცემთა შეტანა")
		self.setWindowIcon(QtGui.QIcon("icon/outcome.svg"))
		self.setFixedSize(1300, 900)
		vbox = QVBoxLayout()
		hbox = QHBoxLayout()
		vbox.setContentsMargins(2, 2, 2, 2)
##################################################### Calendar ####################################################
		self.calendar = QCalendarWidget()
		self.calendar.setGridVisible(True)
		self.calendar.setFirstDayOfWeek(Qt.Monday)
		#self.setCalendarDate(self.date)
####################################################### Table #####################################################
		self.table = QTableWidget()
		self.table.setRowCount(1)
		self.table.setColumnCount(len(self._header))
		self.table.setHorizontalHeaderLabels(self._header)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		#self.table.resizeColumnsToContents()
		self.table.resizeRowsToContents()
		self.table.setSortingEnabled(False)
		self.table.setWordWrap(True)
		self.rowNumb = self.table.rowCount()-1
###################################################### add Row ####################################################
		self.addRowButton = QPushButton('დამატება')
		self.addRowButton.setMaximumWidth(100)
		self.addRowButton.setIcon(QIcon('icon/addRow.png'))
		self.addRowButton.clicked.connect(self.addRow)
###################################################### del Row ####################################################
		self.delRowButton = QPushButton('წაშლა')
		self.delRowButton.setMaximumWidth(100)
		self.delRowButton.setIcon(QIcon('icon/DelRow.png'))
		self.delRowButton.clicked.connect(self.delRow)
####################################################### test ######################################################
		h = QHBoxLayout()
		self.sumMoney = QLineEdit()
		self.equiSumMoney = QLineEdit()
		h.addWidget(self.sumMoney)
		h.addWidget(self.equiSumMoney)
		self.testButton = QPushButton('ტესტი')
		self.testButton.setIcon(QIcon('icon/test.png'))
		self.testButton.clicked.connect(self.test)
####################################################### apply #####################################################
		self.Ok = QPushButton('დადასტურება', self)
		self.Ok.clicked.connect(self.apply)
####################################################### cancel ####################################################
		self.Can = QPushButton('გაუქმება', self)
		self.Can.clicked.connect(self.cancel)

		self.terminal = QPlainTextEdit()

		hbox.addWidget(self.addRowButton)
		hbox.addWidget(self.delRowButton)

		vbox.addWidget(self.calendar,5)
		vbox.addWidget(self.table,90)
		vbox.addLayout(hbox)
		vbox.addLayout(h)
		vbox.addWidget(self.testButton,5)
		hbox_apply_cancel = QHBoxLayout()
		hbox_apply_cancel.addWidget(self.Ok)
		hbox_apply_cancel.addWidget(self.Can)
		vbox.addLayout(hbox_apply_cancel)
		#vbox.addWidget(self.terminal)
		self.setLayout(vbox)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ Add Row ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def addRow(self):
		self.rowNumb = self.table.rowCount()
		self.table.insertRow(self.rowNumb)
		self.addRowWidgets()
#+++++++++++++++++++++++++++++++++++++++++++++++++ Add Row Widgets ++++++++++++++++++++++++++++++++++++++++++++++++
	def addRowWidgets(self):
#################################################### emountEdit ###################################################
		emauntEdit = QLineEdit('1')
		emauntEdit.setMaximumWidth(30)

		unit = QComboBox()
		unit.setToolTip("<h5>ერთეული")
		unit.setMaximumWidth(70)
		unit.addItems(self._units)

		emountEditHlayout = QHBoxLayout()
		emountEditHlayout.addWidget(emauntEdit,20)
		emountEditHlayout.addWidget(unit,80)

		emountEditWidgets = QWidget()
		emountEditWidgets.setLayout(emountEditHlayout)
################################################# Category Selector ###############################################
		CategorySelector = QComboBox()
		CategorySelector.addItems(self._category)
################################################### Price Editor ##################################################
		PriceEdit = QLineEdit()
		PriceEdit.setToolTip("<h5>გადახდა")
		PriceEdit.setMaximumWidth(70)
############################################## Equivalent Price Editor ############################################
		EqviPriceEdit = QLineEdit()
		EqviPriceEdit.setText("--")
		EqviPriceEdit.setToolTip("<h5>კონვერტაცია ვალუტაში")
		EqviPriceEdit.setMaximumWidth(70)
################################################ Currency Selector ################################################
		CurrencySelector = QComboBox()
		for idx, key in enumerate(self._Currency):
			CurrencySelector.addItem(key)
			CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
			CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))
########################################### Equivalent Currency Selector ##########################################
		EqviCurrencySelector = QComboBox()
		for idx, key in enumerate(self._Currency):
			EqviCurrencySelector.addItem(key)
			EqviCurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
			EqviCurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))
############################################### App widgets in cells ##############################################
		priceHlayout = QHBoxLayout()
		priceHlayout.addWidget(PriceEdit)
		priceHlayout.addWidget(CurrencySelector)
		priceHlayout.addWidget(EqviPriceEdit)
		priceHlayout.addWidget(EqviCurrencySelector)

		priceWidgets = QWidget()
		priceWidgets.setLayout(priceHlayout)

		PayMethodWidgets = QWidget()

		PayMethod = QCheckBox()
		PayMethod.setToolTip("<h5>ნაღდით გადახდა")
		PayMethodHlayout = QHBoxLayout()
		PayMethodHlayout.addWidget(PayMethod)
		PayMethodHlayout.setAlignment( Qt.AlignCenter )
		PayMethodWidgets.setLayout(PayMethodHlayout)

		eventContent = QTableWidgetItem('')
		self.table.setItem(self.rowNumb, 0, eventContent)
		eventContent.setData(Qt.UserRole, random.sample(self._EventNames, len(self._EventNames)))
		self.table.setItemDelegate(TableItemCompleter(self.table))

		self.table.setCellWidget(self.rowNumb, 1, emountEditWidgets)
		self.table.setCellWidget(self.rowNumb, 2, CategorySelector)
		self.table.setCellWidget(self.rowNumb, 3, priceWidgets)
		self.table.setCellWidget(self.rowNumb, 4, PayMethodWidgets)
############################################### Set Table Cell Widths #############################################
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

		self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
		self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
		self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
#++++++++++++++++++++++++++++++++++++++++++++++++++++ Delete Row ++++++++++++++++++++++++++++++++++++++++++++++++++
	def delRow(self):
		self.rowNumb = self.table.rowCount()
		if self.rowNumb > 1:
			selected_Row = self.table.currentRow()
			self.table.removeRow(selected_Row)
#++++++++++++++++++++++++++++++++++++++++++++++++ Set calendar date +++++++++++++++++++++++++++++++++++++++++++++++
	def setCalendarDate(self, date):
		self.calendar.setSelectedDate(QDate(date[0], date[1], date[2]))
#++++++++++++++++++++++++++++++++++++++++++++++++++++ Terminal ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def term(self, Text):
		self.terminal.insertPlainText("-----------------------------\n")
		self.terminal.insertPlainText("----> " + Text + "\n")
		self.terminal.insertPlainText("-----------------------------\n")
#+++++++++++++++++++++++++++++++++++++++++++++++ Make data claster ++++++++++++++++++++++++++++++++++++++++++++++++
	def makeDataClaster(self):
		self.dataContainer = {}
		dataContainerArray = []
		self.rowNumb = self.table.rowCount()
		self.colNumb = self.table.columnCount()
		for row in range(self.rowNumb):
			dataContainerTemp = []
			for column in range(self.colNumb):
				if column == 0:
					dataContainerTemp.append({ 'cell_0'   : self.table.item(row,column).text()})
				elif column == 1:
					dataContainerTemp.append({	'cell_1.1' : self.table.cellWidget(row,column).children()[1].text(),
												'cell_1.2' : self.table.cellWidget(row,column).children()[2].currentIndex()})
				elif column == 2:
					dataContainerTemp.append({	'cell_2.1' : self.table.cellWidget(row,column).currentIndex()})
				elif column == 3:
					dataContainerTemp.append({	'cell_3.1' : self.table.cellWidget(row,column).children()[1].text(),
												'cell_3.2' : self.table.cellWidget(row,column).children()[2].currentIndex(),
												'cell_3.3' : self.table.cellWidget(row,column).children()[3].text(),
												'cell_3.4' : self.table.cellWidget(row,column).children()[4].currentIndex()})
				elif column == 4:
					dataContainerTemp.append({	'cell_4'   : self.table.cellWidget(row,column).children()[1].isChecked()})
			dataContainerArray.append(dataContainerTemp)
		self.dataContainer.update({self.calendar.selectedDate().toString("dd.MM.yyyy") : dataContainerArray})
		#self.term(pformat(self.dataContainer, indent=4))
#+++++++++++++++++++++++++++++++++++++++++++++++ Edit data claster ++++++++++++++++++++++++++++++++++++++++++++++++
	def EditDataClaster(self, DataClasterComponent, timeStamp):
		for rowNumber in range(len(DataClasterComponent)-1):
			self.addRow()
		self.setCalendarDate(QDate.fromString(timeStamp, 'dd.MM.yyyy').getDate())
		for row in range(len(DataClasterComponent)):
			self.table.item(row, 0).setText(DataClasterComponent[row][0]['cell_0'])
			self.table.cellWidget(row, 1).children()[1].setText(DataClasterComponent[row][1]['cell_1.1'])
			self.table.cellWidget(row, 1).children()[2].setCurrentIndex(DataClasterComponent[row][1]['cell_1.2'])
			self.table.cellWidget(row, 2).setCurrentIndex(DataClasterComponent[row][2]['cell_2.1'])
			self.table.cellWidget(row, 3).children()[1].setText(DataClasterComponent[row][3]['cell_3.1'])
			self.table.cellWidget(row, 3).children()[2].setCurrentIndex(DataClasterComponent[row][3]['cell_3.2'])
			self.table.cellWidget(row, 3).children()[3].setText(DataClasterComponent[row][3]['cell_3.3'])
			self.table.cellWidget(row, 3).children()[4].setCurrentIndex(DataClasterComponent[row][3]['cell_3.4'])
			self.table.cellWidget(row, 4).children()[1].setChecked(DataClasterComponent[row][4]['cell_4'])
#++++++++++++++++++++++++++++++++++++++++++++++++++++++ Apply +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def apply(self):
		self.makeDataClaster()
		self.applayState = True
		self.close()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ Cancel +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def cancel(self):
		self.applayState = False
		self.close()
#+++++++++++++++++++++++++++++++++++++++++++++ Get data claster part ++++++++++++++++++++++++++++++++++++++++++++++
	def getDataClasterPart(self):
		return self.dataContainer, self.applayState
#++++++++++++++++++++++++++++++++++++++++++++++++++++++ Test ++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def test(self):
		print("Test")
		data =  {'22.01.1993': [  [	{'cell_0': 'პური'},
									{'cell_1.1': '2', 'cell_1.2': 1},
									{'cell_2.1': 2},
									{   'cell_3.1': '30',
										'cell_3.2': 1,
										'cell_3.3': '100',
										'cell_3.4': 0},
									{'cell_4': True}],
								  [ {'cell_0': 'ლობიო'},
									{'cell_1.1': '5', 'cell_1.2': 1},
									{'cell_2.1': 3},
									{   'cell_3.1': '64',
										'cell_3.2': 2,
										'cell_3.3': '54',
										'cell_3.4': 3},
									{'cell_4': True}]]}
		#self.EditDataClaster(data)
		self.makeDataClaster()
		self.rowNumb = self.table.rowCount()
		sumMoney = 0
		equiSumMoney = 0
		for row in range(self.rowNumb):
			try:
				sumMoney = sumMoney + round(float(self.table.cellWidget(row,3).children()[1].text()), 2)
			except ValueError:
				pass
			try:
				equiSumMoney = equiSumMoney + round(float(self.table.cellWidget(row,3).children()[3].text()), 2)
			except ValueError:
				pass
		self.sumMoney.setText(str(sumMoney))
		self.equiSumMoney.setText(str(equiSumMoney))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Enter Income Event Claster ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class IncomeEventClaster(QDialog):
	def __init__(self, parent = None):
		QDialog.__init__(self, parent)
		self.applayState = False
		self.dataContainer = {}
		self._header = ['წყარო','რაოდენობა']
		self._IncomeSourceCategory = ['ავანსი','ხელფასი','პრემია','მივლინება','ქეშბექი','საჩუქარი','ვალის დაბრუნება','კონვერტაცია','პრიზი','სხვა']
		self._Currency = {	'₽'  : 'icon/Ruble.png',
							'$'  : 'icon/Dollar.png',
							'€'  : 'icon/Euro.png',
							'CHF': 'icon/swiss-franc.png',
							'₾'  : 'icon/Lari.png',
							'¥'  : 'icon/yuan.png'}
		self.date = [1993,1,22]

		self.InitUI()
		self.addRowWidgets()
		self.show()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ InitUI +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def InitUI(self):
		self.setWindowTitle("მონაცემთა შეტანა")
		self.setWindowIcon(QtGui.QIcon("icon/income.svg"))
		self.setFixedSize(800, 900)
		vbox = QVBoxLayout()
		hbox = QHBoxLayout()
		vbox.setContentsMargins(2, 2, 2, 2)
##################################################### Calendar ####################################################
		self.calendar = QCalendarWidget()
		self.calendar.setGridVisible(True)
		self.calendar.setFirstDayOfWeek(Qt.Monday)
		#self.setCalendarDate(self.date)
####################################################### Table #####################################################
		self.table = QTableWidget()
		self.table.setRowCount(1)
		self.table.setColumnCount(len(self._header))
		self.table.setHorizontalHeaderLabels(self._header)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.table.resizeRowsToContents()
		self.table.setSortingEnabled(False)
		self.table.setWordWrap(True)
		self.rowNumb = self.table.rowCount()-1
###################################################### add Row ####################################################
		self.addRowButton = QPushButton('დამატება')
		self.addRowButton.setMaximumWidth(100)
		self.addRowButton.setIcon(QIcon('icon/addRow.png'))
		self.addRowButton.clicked.connect(self.addRow)
###################################################### del Row ####################################################
		self.delRowButton = QPushButton('წაშლა')
		self.delRowButton.setMaximumWidth(100)
		self.delRowButton.setIcon(QIcon('icon/DelRow.png'))
		self.delRowButton.clicked.connect(self.delRow)
######################################################## test #####################################################
		self.testButton = QPushButton('ტესტი')
		self.testButton.setIcon(QIcon('icon/test.png'))
		self.testButton.clicked.connect(self.test)
####################################################### apply #####################################################
		self.Ok = QPushButton('დადასტურება', self)
		self.Ok.clicked.connect(self.apply)
####################################################### cancel ####################################################
		self.Can = QPushButton('გაუქმება', self)
		self.Can.clicked.connect(self.cancel)

		self.terminal = QPlainTextEdit()

		hbox.addWidget(self.addRowButton)
		hbox.addWidget(self.delRowButton)

		vbox.addWidget(self.calendar,5)
		vbox.addWidget(self.table,90)
		vbox.addLayout(hbox)
		vbox.addWidget(self.testButton,5)
		hbox_apply_cancel = QHBoxLayout()
		hbox_apply_cancel.addWidget(self.Ok)
		hbox_apply_cancel.addWidget(self.Can)
		vbox.addLayout(hbox_apply_cancel)
		vbox.addWidget(self.terminal)
		self.setLayout(vbox)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ Add Row ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def addRow(self):
		self.rowNumb = self.table.rowCount()
		self.table.insertRow(self.rowNumb)
		self.addRowWidgets()
#+++++++++++++++++++++++++++++++++++++++++++++++++ Add Row Widgets ++++++++++++++++++++++++++++++++++++++++++++++++
	def addRowWidgets(self):
#################################################### emountEdit ###################################################
		emauntEdit = QLineEdit('')
################################################ Currency Selector ################################################
		CurrencySelector = QComboBox()
		for idx, key in enumerate(self._Currency):
			CurrencySelector.addItem(key)
			CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
			CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))

		emountEditHlayout = QHBoxLayout()
		emountEditHlayout.addWidget(emauntEdit,50)
		emountEditHlayout.addWidget(CurrencySelector,50)

		emountEditWidgets = QWidget()
		emountEditWidgets.setLayout(emountEditHlayout)
############################################# Income Category Selector ############################################
		IncomeCategorySelector = QComboBox()
		IncomeCategorySelector.addItems(self._IncomeSourceCategory)

		self.table.setCellWidget(self.rowNumb, 0, IncomeCategorySelector)
		self.table.setCellWidget(self.rowNumb, 1, emountEditWidgets)
############################################### Set Table Cell Widths #############################################
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
#++++++++++++++++++++++++++++++++++++++++++++++++++++ Delete Row ++++++++++++++++++++++++++++++++++++++++++++++++++
	def delRow(self):
		self.rowNumb = self.table.rowCount()
		if self.rowNumb > 1:
			selected_Row = self.table.currentRow()
			self.table.removeRow(selected_Row)
#++++++++++++++++++++++++++++++++++++++++++++++++ Set calendar date +++++++++++++++++++++++++++++++++++++++++++++++
	def setCalendarDate(self, date):
		self.calendar.setSelectedDate(QDate(date[0], date[1], date[2]))
#++++++++++++++++++++++++++++++++++++++++++++++++++++ Terminal ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def term(self, Text):
		self.terminal.insertPlainText("-----------------------------\n")
		self.terminal.insertPlainText("----> " + Text + "\n")
		self.terminal.insertPlainText("-----------------------------\n")
#+++++++++++++++++++++++++++++++++++++++++++++++ Make data claster ++++++++++++++++++++++++++++++++++++++++++++++++
	def makeDataClaster(self):
		self.dataContainer = {}
		dataContainerArray = []
		self.rowNumb = self.table.rowCount()
		self.colNumb = self.table.columnCount()
		for row in range(self.rowNumb):
			dataContainerTemp = []
			for column in range(self.colNumb):
				if column == 0:
					dataContainerTemp.append({ 'cell_0'   : self.table.cellWidget(row,column).currentIndex()})
				elif column == 1:
					dataContainerTemp.append({	'cell_1.1' : self.table.cellWidget(row,column).children()[1].text(),
												'cell_1.2' : self.table.cellWidget(row,column).children()[2].currentIndex()})
			dataContainerArray.append(dataContainerTemp)
		self.dataContainer.update({self.calendar.selectedDate().toString("dd.MM.yyyy") : dataContainerArray})
		self.term(pformat(self.dataContainer, indent=4))
#+++++++++++++++++++++++++++++++++++++++++++++++ Edit data claster ++++++++++++++++++++++++++++++++++++++++++++++++
	def EditDataClaster(self, DataClasterComponent, timeStamp):
		for rowNumber in range(len(DataClasterComponent)-1):
			self.addRow()
		self.setCalendarDate(QDate.fromString(timeStamp, 'dd.MM.yyyy').getDate())
		for row in range(len(DataClasterComponent)):
			self.table.cellWidget(row, 0).setCurrentIndex(DataClasterComponent[row][0]['cell_0'])
			self.table.cellWidget(row, 1).children()[1].setText(DataClasterComponent[row][1]['cell_1.1'])
			self.table.cellWidget(row, 1).children()[2].setCurrentIndex(DataClasterComponent[row][1]['cell_1.2'])
#++++++++++++++++++++++++++++++++++++++++++++++++++++++ Apply +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def apply(self):
		self.makeDataClaster()
		self.applayState = True
		self.close()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++ Cancel +++++++++++++++++++++++++++++++++++++++++++++++++++++
	def cancel(self):
		self.applayState = False
		self.close()
#+++++++++++++++++++++++++++++++++++++++++++++ Get data claster part ++++++++++++++++++++++++++++++++++++++++++++++
	def getDataClasterPart(self):
		return self.dataContainer, self.applayState
#++++++++++++++++++++++++++++++++++++++++++++++++++++++ Test ++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def test(self):
		print("Test")

		data =  {   '22.01.1993': [[{'cell_0': 0},
									{'cell_1.1': '16500', 'cell_1.2': 0}],
								   [{'cell_0': 2},
									{'cell_1.1': '6000', 'cell_1.2': 0}]]}
		#self.EditDataClaster(data)
		self.makeDataClaster()


if __name__ == '__main__':
	App = QApplication(sys.argv)
	App.setStyle('Fusion')
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
	App.setPalette(palette)
	
	Window = OutcomeEventClaster()
	#Window = IncomeEventClaster()
	sys.exit(App.exec_())