from PyQt5.QtWidgets import QApplication, QHeaderView, QDateTimeEdit, QDateTimeEdit, QHeaderView, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDateTime
import sys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TableView ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OutcomeTable(QTableWidget):
# ++++++++++++++++++++++++++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def __init__(self):
		QTableWidget.__init__(self)
		self._Currency = {	0 : '₽',
							1 : '$',
							2 : '€',
							3 : 'CHF',
							4 : '₾',
							5 : '¥'}
		self._header = ['დრო','მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
		self._units = ['--','ც','კგ','გრ','ლ','მლ','კვტ','თვე','დღე']
		self._category = [	'კვება','სხვადასხვა','ქირა','საყოფაცხოვრებო','კომუნალური','ტელეფონი',
							'ინტერნეტი','გართობა','ტანსაცმელი','ჰიგიენა','მედიკამენტები','ინტერნეტი',
							'ტრანსპორტი','მოწყობილობები','დასვენება','საჩუქარი','გამოწერა','საკომისიო','აღჭურვილობა',
							'ვარჯიში','რემონტი','ექიმთან კონსულტაცია','მკურნალობა','ჯარიმა','მოგზაურობა','გასესხება','გასესხებულის დაბრუნება','სესხი','სესხის დაბრუნება']
		self.setColumnCount(len(self._header))
		self.setHorizontalHeaderLabels(self._header)
		self.setSortingEnabled(False)
		self.setWordWrap(True)
# ++++++++++++++++++++++++++++++++++++++++++++++++++ importEvents ++++++++++++++++++++++++++++++++++++++++++++++++++
	def importEvents(self, data):
		self.setRowCount(0)
		TimeStampsIndex = 0
		for key in data:
			self.rowNumb = self.rowCount()
			self.setRowCount(self.rowNumb + len(data[key]))

			timeStamp = QDateTimeEdit()
			timeStamp.setDisplayFormat("dd.MM.yyyy")
			timeStamp.setReadOnly(True)
			timeStampCell = QDateTime.currentDateTime()
			timeStampCell = QDateTime.fromString(key, "dd.MM.yyyy")
			timeStamp.setDateTime(timeStampCell)
			self.setCellWidget(TimeStampsIndex, 0, timeStamp)
			if len(data[key]) > 1:
				self.setSpan(TimeStampsIndex, 0, len(data[key]) , 1)
			
			for row in range(len(data[key])):
				cell_0 = QTableWidgetItem('')
				cell_0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_0.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				cell_1 = QTableWidgetItem('')
				cell_1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_1.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				cell_2 = QTableWidgetItem('')
				cell_2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_2.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				cell_3 = QTableWidgetItem('')
				cell_3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_3.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				cell_4 = QTableWidgetItem('')
				if data[key][row][4]['cell_4']:
					cell_4.setIcon(QtGui.QIcon('icon/cash.svg'))
				else:
					cell_4.setIcon(QtGui.QIcon('icon/card.svg'))
				
				cell_4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_4.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				self.setItem(TimeStampsIndex + row, 1, cell_0)
				self.setItem(TimeStampsIndex + row, 2, cell_1)
				self.setItem(TimeStampsIndex + row, 3, cell_2)
				self.setItem(TimeStampsIndex + row, 4, cell_3)
				self.setItem(TimeStampsIndex + row, 5, cell_4)

				self.item(TimeStampsIndex + row, 1).setText(data[key][row][0]['cell_0'])
				if self._units[data[key][row][1]['cell_1.2']] == "--":
					self.item(TimeStampsIndex + row, 2).setText(self._units[data[key][row][1]['cell_1.2']])
				else:
					self.item(TimeStampsIndex + row, 2).setText(data[key][row][1]['cell_1.1'] + self._units[data[key][row][1]['cell_1.2']])
				self.item(TimeStampsIndex + row, 3).setText(self._category[data[key][row][2]['cell_2.1']])
				try:
					if data[key][row][3]['cell_3.3'] == "--" or data[key][row][3]['cell_3.3'] == "":
						self.item(TimeStampsIndex + row, 4).setText("%.2f" % round(float(data[key][row][3]['cell_3.1']), 2) + self._Currency[data[key][row][3]['cell_3.2']])
					else:
						self.item(TimeStampsIndex + row, 4).setText("%.2f" % round(float(data[key][row][3]['cell_3.1']), 2) + self._Currency[data[key][row][3]['cell_3.2']] + " ---> " + "%.2f" % round(float(data[key][row][3]['cell_3.3']), 2) + self._Currency[data[key][row][3]['cell_3.4']])
				except ValueError:
					pass
				if data[key][row][4]['cell_4']:
					self.item(TimeStampsIndex + row, 5).setText("Cash")
				else:
					self.item(TimeStampsIndex + row, 5).setText("Card")
			
			TimeStampsIndex = TimeStampsIndex + len(data[key])

		self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
		self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
		self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
		self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
		self.scrollToBottom()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IncomeTable ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class IncomeTable(QTableWidget):
# ++++++++++++++++++++++++++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++++++++++++++++++++++++
	def __init__(self):
		QTableWidget.__init__(self)
		self._Currency = {	0 : '₽',
							1 : '$',
							2 : '€',
							3 : 'CHF',
							4 : '₾',
							5 : '¥'}
		self._header = ['დრო','წყარო','რაოდენობა']
		self._IncomeSourceCategory = ['ავანსი','ხელფასი','პრემია','მივლინება','ქეშბექი','საჩუქარი','ვალის დაბრუნება','კონვერტაცია','პრიზი','სხვა']
		self.setColumnCount(len(self._header))
		self.setHorizontalHeaderLabels(self._header)
		self.setSortingEnabled(False)
		self.setWordWrap(True)
# ++++++++++++++++++++++++++++++++++++++++++++++++++ importEvents ++++++++++++++++++++++++++++++++++++++++++++++++++
	def importEvents(self, data):
		self.setRowCount(0)
		TimeStampsIndex = 0
		for key in data:
			self.rowNumb = self.rowCount()
			self.setRowCount(self.rowNumb + len(data[key]))

			timeStamp = QDateTimeEdit()
			timeStamp.setDisplayFormat("dd.MM.yyyy")
			timeStamp.setReadOnly(True)
			timeStampCell = QDateTime.currentDateTime()
			timeStampCell = QDateTime.fromString(key, "dd.MM.yyyy")
			timeStamp.setDateTime(timeStampCell)
			self.setCellWidget(TimeStampsIndex, 0, timeStamp)
			if len(data[key]) > 1:
				self.setSpan(TimeStampsIndex, 0, len(data[key]) , 1)

			for row in range(len(data[key])):
				cell_0 = QTableWidgetItem('')
				cell_0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_0.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				cell_1 = QTableWidgetItem('')
				cell_1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				cell_1.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )

				self.setItem(TimeStampsIndex + row, 1, cell_0)
				self.setItem(TimeStampsIndex + row, 2, cell_1)

				self.item(TimeStampsIndex + row, 1).setText(self._IncomeSourceCategory[data[key][row][0]['cell_0']])
				try:
					self.item(TimeStampsIndex + row, 2).setText("%.2f" % round(float(data[key][row][1]['cell_1.1']), 2) + self._Currency[data[key][row][1]['cell_1.2']])
				except ValueError:
					pass
			TimeStampsIndex = TimeStampsIndex + len(data[key])

		self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
		self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
		self.scrollToBottom()
####################################################################################################################
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = OutcomeTable()
	#ex = IncomeTable()
	ex.setGeometry(400,200,900,500)
	ex.show()
	sys.exit(app.exec_())