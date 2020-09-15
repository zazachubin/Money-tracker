from PyQt5.QtWidgets import (	QApplication, QHeaderView, QDialog, QWidget, QLineEdit, QStyledItemDelegate, 
                                QPushButton, QComboBox, QCheckBox, QCompleter, QCalendarWidget, QHBoxLayout,
                                QVBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QColor, QPalette, QIcon, QDoubleValidator
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Enter Info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OutcomeEventClaster(QDialog):
    def __init__(self, header, outComeEventNames, outComeCategory, units, currency, parent = None):
        QDialog.__init__(self, parent)
        self._acceptState = False
        self._dataContainer = {}
        self._header = header
        self._Currency = currency
        self._units = units
        self._category = outComeCategory
        self._EventNames = outComeEventNames
        
        self.InitUI()
        self.addRowWidgets()
        self.show()
#++++++++++++++++++++++++++++++ InitUI ++++++++++++++++++++++++++++++++
    def InitUI(self):
        self.setWindowTitle("მონაცემთა შეტანა")
        self.setWindowIcon(QtGui.QIcon("icon/outcome.svg"))
        self.setFixedSize(1300, 900)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.setContentsMargins(2, 2, 2, 2)
############################## Calendar ###############################
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
############################### Table #################################
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(len(self._header))
        self.table.setHorizontalHeaderLabels(self._header)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(False)
        self.table.setWordWrap(True)
        self.rowNumb = self.table.rowCount()-1
############################## add Row ################################
        self.addRowButton = QPushButton('დამატება')
        self.addRowButton.setMaximumWidth(100)
        self.addRowButton.setIcon(QIcon('icon/addRow.svg'))
        self.addRowButton.clicked.connect(self.addRow)
############################## del Row ################################
        self.delRowButton = QPushButton('წაშლა')
        self.delRowButton.setMaximumWidth(100)
        self.delRowButton.setIcon(QIcon('icon/DelRow.svg'))
        self.delRowButton.clicked.connect(self.delRow)
############################### test ##################################
        sumHboxLayout = QHBoxLayout()
        self.sumMoney = QLineEdit()
        self.equivalentSumMoney = QLineEdit()
        sumHboxLayout.addWidget(self.sumMoney)
        sumHboxLayout.addWidget(self.equivalentSumMoney)
        self.testButton = QPushButton('ტესტი')
        self.testButton.setIcon(QIcon('icon/test.png'))
        self.testButton.clicked.connect(self.test)
############################## Accept #################################
        self.acceptButton = QPushButton('დადასტურება', self)
        self.acceptButton.clicked.connect(self.acceptDialog)
############################## Reject #################################
        self.rejectButton = QPushButton('გაუქმება', self)
        self.rejectButton.clicked.connect(self.rejectDialog)
###################### Add widgets on layouts #########################
        hbox.addWidget(self.addRowButton)
        hbox.addWidget(self.delRowButton)

        vbox.addWidget(self.calendar,5)
        vbox.addWidget(self.table,90)
        vbox.addLayout(hbox)
        vbox.addLayout(sumHboxLayout)
        vbox.addWidget(self.testButton,5)
        hboxAcceptReject = QHBoxLayout()
        hboxAcceptReject.addWidget(self.acceptButton)
        hboxAcceptReject.addWidget(self.rejectButton)
        vbox.addLayout(hboxAcceptReject)
        self.setLayout(vbox)
#++++++++++++++++++++++++++++ Add Row +++++++++++++++++++++++++++++++++
    def addRow(self):
        self.rowNumb = self.table.rowCount()
        self.table.insertRow(self.rowNumb)
        self.addRowWidgets()
#++++++++++++++++++++++++ Add Row Widgets +++++++++++++++++++++++++++++
    def addRowWidgets(self):
########################### emountEdit ################################
        quantityEdit = QLineEdit('1')
        quantityEdit.setValidator(QDoubleValidator())
        quantityEdit.setMaximumWidth(30)

        units = QComboBox()
        units.setToolTip("<h5>ერთეული")
        units.setMaximumWidth(70)
        units.addItems(self._units)

        quantityEditHlayout = QHBoxLayout()
        quantityEditHlayout.addWidget(quantityEdit,20)
        quantityEditHlayout.addWidget(units,80)

        quantityEditWidgets = QWidget()
        quantityEditWidgets.setLayout(quantityEditHlayout)
####################### Category Selector #############################
        outcomeCategorySelector = QComboBox()
        outcomeCategorySelector.addItems(self._category)
########################## Price Editor ###############################
        PriceEdit = QLineEdit()
        PriceEdit.setValidator(QDoubleValidator())
        PriceEdit.setToolTip("<h5>გადახდა")
        PriceEdit.setMaximumWidth(70)
#################### Equivalent Price Editor ##########################
        equivalentPriceEdit = QLineEdit()
        equivalentPriceEdit.setValidator(QDoubleValidator())
        equivalentPriceEdit.setText("--")
        equivalentPriceEdit.setToolTip("<h5>კონვერტაცია ვალუტაში")
        equivalentPriceEdit.setMaximumWidth(70)
####################### Currency Selector #############################
        CurrencySelector = QComboBox()
        for idx, key in enumerate(self._Currency):
            CurrencySelector.addItem(key)
            CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
            CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))
################# Equivalent Currency Selector ########################
        EqviCurrencySelector = QComboBox()
        for idx, key in enumerate(self._Currency):
            EqviCurrencySelector.addItem(key)
            EqviCurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
            EqviCurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))
###################### App widgets in cells ###########################
        priceHlayout = QHBoxLayout()
        priceHlayout.addWidget(PriceEdit)
        priceHlayout.addWidget(CurrencySelector)
        priceHlayout.addWidget(equivalentPriceEdit)
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

        self.table.setCellWidget(self.rowNumb, 1, quantityEditWidgets)
        self.table.setCellWidget(self.rowNumb, 2, outcomeCategorySelector)
        self.table.setCellWidget(self.rowNumb, 3, priceWidgets)
        self.table.setCellWidget(self.rowNumb, 4, PayMethodWidgets)
###################### Set Table Cell Widths ##########################
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
# +++++++++++++ String to float number formater +++++++++++++++++++++++
    def _stingToFloatFormater(self, value):
        if ',' in value:
            value = value.replace(",", ".")
            return value
        else:
            return value
#++++++++++++++++++++++++++ Delete Row ++++++++++++++++++++++++++++++++
    def delRow(self):
        self.rowNumb = self.table.rowCount()
        if self.rowNumb > 1:
            selected_Row = self.table.currentRow()
            self.table.removeRow(selected_Row)
#++++++++++++++++++++++ Set calendar date +++++++++++++++++++++++++++++
    def setCalendarDate(self, date):
        self.calendar.setSelectedDate(QDate(date[0], date[1], date[2]))
#++++++++++++++++++++++ Make data claster +++++++++++++++++++++++++++++
    def makeDataClaster(self):
        self._dataContainer = {}
        dataContainerArray = []
        self.rowNumb = self.table.rowCount()
        self.colNumb = self.table.columnCount()
        for row in range(self.rowNumb):
            dataContainerTemp = []
            for column in range(self.colNumb):
                if column == 0:
                    dataContainerTemp.append({'cell_0'   : self.table.item(row,column).text()})
                elif column == 1:
                    dataContainerTemp.append({'cell_1.1' : self._stingToFloatFormater(self.table.cellWidget(row,column).children()[1].text()),
                                              'cell_1.2' : self.table.cellWidget(row,column).children()[2].currentIndex()})
                elif column == 2:
                    dataContainerTemp.append({'cell_2.1' : self.table.cellWidget(row,column).currentIndex()})
                elif column == 3:
                    dataContainerTemp.append({'cell_3.1' : self._stingToFloatFormater(self.table.cellWidget(row,column).children()[1].text()),
                                              'cell_3.2' : self.table.cellWidget(row,column).children()[2].currentIndex(),
                                              'cell_3.3' : self._stingToFloatFormater(self.table.cellWidget(row,column).children()[3].text()),
                                              'cell_3.4' : self.table.cellWidget(row,column).children()[4].currentIndex()})
                elif column == 4:
                    dataContainerTemp.append({'cell_4'   : self.table.cellWidget(row,column).children()[1].isChecked()})
            dataContainerArray.append(dataContainerTemp)
        self._dataContainer.update({self.calendar.selectedDate().toString("dd.MM.yyyy") : dataContainerArray})
#++++++++++++++++++++++ Edit data claster +++++++++++++++++++++++++++++
    def EditDataClaster(self, DataClasterComponent, timeStamp):
        for _ in range(len(DataClasterComponent)-1):
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
#+++++++++++++++++++++++++++ Accept +++++++++++++++++++++++++++++++++++
    def acceptDialog(self):
        self.makeDataClaster()
        self._acceptState = True
        self.close()
#+++++++++++++++++++++++++++ Reject +++++++++++++++++++++++++++++++++++
    def rejectDialog(self):
        self._acceptState = False
        self.close()
#++++++++++++++++++++ Get data claster part +++++++++++++++++++++++++++
    def getDataClasterPart(self):
        return self._dataContainer, self._acceptState
#++++++++++++++++++++++++++++ Test ++++++++++++++++++++++++++++++++++++
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
        self.equivalentSumMoney.setText(str(equiSumMoney))

# ~~~~~~~~~~~~~~~~ Enter Income Event Claster ~~~~~~~~~~~~~~~~~~~~~~~~~
class IncomeEventClaster(QDialog):
    def __init__(self, header, IncomeSourceCategory, currency, parent = None):
        QDialog.__init__(self, parent)
        self._acceptState = False
        self._dataContainer = {}
        self._header = header
        self._IncomeSourceCategory = IncomeSourceCategory
        self._Currency = currency
        self.date = [1993,1,22]

        self.InitUI()
        self.addRowWidgets()
        self.show()
#+++++++++++++++++++++++++++ InitUI +++++++++++++++++++++++++++++++++++
    def InitUI(self):
        self.setWindowTitle("მონაცემთა შეტანა")
        self.setWindowIcon(QtGui.QIcon("icon/income.svg"))
        self.setFixedSize(750, 900)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.setContentsMargins(2, 2, 2, 2)
########################### Calendar ##################################
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
############################ Table ####################################
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(len(self._header))
        self.table.setHorizontalHeaderLabels(self._header)
        self.table.setSortingEnabled(False)
        self.table.setWordWrap(True)
        self.rowNumb = self.table.rowCount()-1
########################### add Row ###################################
        self.addRowButton = QPushButton('დამატება')
        self.addRowButton.setMaximumWidth(100)
        self.addRowButton.setIcon(QIcon('icon/addRow.svg'))
        self.addRowButton.clicked.connect(self.addRow)
########################### del Row ###################################
        self.delRowButton = QPushButton('წაშლა')
        self.delRowButton.setMaximumWidth(100)
        self.delRowButton.setIcon(QIcon('icon/DelRow.svg'))
        self.delRowButton.clicked.connect(self.delRow)
############################# test ####################################
        self.testButton = QPushButton('ტესტი')
        self.testButton.setIcon(QIcon('icon/test.png'))
        self.testButton.clicked.connect(self.test)
############################ Accept ###################################
        self.acceptButton = QPushButton('დადასტურება', self)
        self.acceptButton.clicked.connect(self.acceptDialog)
############################ Reject ###################################
        self.rejectButton = QPushButton('გაუქმება', self)
        self.rejectButton.clicked.connect(self.rejectDialog)
#################### Add widgets on layouts ###########################
        hbox.addWidget(self.addRowButton)
        hbox.addWidget(self.delRowButton)

        vbox.addWidget(self.calendar,5)
        vbox.addWidget(self.table,90)
        vbox.addLayout(hbox)
        vbox.addWidget(self.testButton,5)
        hboxAcceptReject = QHBoxLayout()
        hboxAcceptReject.addWidget(self.acceptButton)
        hboxAcceptReject.addWidget(self.rejectButton)
        vbox.addLayout(hboxAcceptReject)
        self.setLayout(vbox)
#++++++++++++++++++++++++++ Add Row +++++++++++++++++++++++++++++++++++
    def addRow(self):
        self.rowNumb = self.table.rowCount()
        self.table.insertRow(self.rowNumb)
        self.addRowWidgets()
#++++++++++++++++++++++ Add Row Widgets +++++++++++++++++++++++++++++++
    def addRowWidgets(self):
########################## emountEdit #################################
        quantityEdit = QLineEdit('')
        quantityEdit.setValidator(QDoubleValidator())
###################### Currency Selector ##############################
        CurrencySelector = QComboBox()
        for idx, key in enumerate(self._Currency):
            CurrencySelector.addItem(key)
            CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
            CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))

        quantityEditHlayout = QHBoxLayout()
        quantityEditHlayout.addWidget(quantityEdit,50)
        quantityEditHlayout.addWidget(CurrencySelector,50)

        quantityEditWidgets = QWidget()
        quantityEditWidgets.setLayout(quantityEditHlayout)
################## Income Category Selector ###########################
        incomeCategorySelector = QComboBox()
        incomeCategorySelector.addItems(self._IncomeSourceCategory)

        self.table.setCellWidget(self.rowNumb, 0, incomeCategorySelector)
        self.table.setCellWidget(self.rowNumb, 1, quantityEditWidgets)
        self.table.cellWidget(self.rowNumb,0).activated.connect(self.incomeCategoryFormater)
################### Set Table Cell Widths #############################
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
# +++++++++++++ String to float number formater +++++++++++++++++++++++
    def _stingToFloatFormater(self, value):
        if ',' in value:
            value = value.replace(",", ".")
            return value
        else:
            return value
#++++++++++++++++++++++++ Delete Row ++++++++++++++++++++++++++++++++++
    def delRow(self):
        self.rowNumb = self.table.rowCount()
        if self.rowNumb > 1:
            selected_Row = self.table.currentRow()
            self.table.removeRow(selected_Row)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
#+++++++++++++++++++++ Set calendar date ++++++++++++++++++++++++++++++
    def setCalendarDate(self, date):
        self.calendar.setSelectedDate(QDate(date[0], date[1], date[2]))
#+++++++++++++++++++++ Make data claster ++++++++++++++++++++++++++++++
    def makeDataClaster(self):
        self._dataContainer = {}
        dataContainerArray = []
        self.rowNumb = self.table.rowCount()
        self.colNumb = self.table.columnCount()
        for row in range(self.rowNumb):
            dataContainerTemp = []
            for column in range(self.colNumb):
                if column == 0:
                    dataContainerTemp.append({'cell_0'   : self.table.cellWidget(row,column).currentIndex()})
                elif column == 1:
                    if len(self.table.cellWidget(row, 1).children()[0]) == 2:
                        dataContainerTemp.append({'cell_1.1' : self.table.cellWidget(row,column).children()[1].text(),
                                                  'cell_1.2' : self.table.cellWidget(row,column).children()[2].currentIndex()})
                    elif len(self.table.cellWidget(row, 1).children()[0]) == 4:
                        dataContainerTemp.append({'cell_1.1' : self._stingToFloatFormater(self.table.cellWidget(row,column).children()[1].text()),
                                                  'cell_1.2' : self.table.cellWidget(row,column).children()[2].currentIndex(),
                                                  'cell_1.3' : self._stingToFloatFormater(self.table.cellWidget(row,column).children()[3].text()),
                                                  'cell_1.4' : self.table.cellWidget(row,column).children()[4].currentIndex()})
            dataContainerArray.append(dataContainerTemp)
        self._dataContainer.update({self.calendar.selectedDate().toString("dd.MM.yyyy") : dataContainerArray})
#+++++++++++++++++++++ Edit data claster ++++++++++++++++++++++++++++++
    def EditDataClaster(self, DataClasterComponent, timeStamp):
        for _ in range(len(DataClasterComponent)-1):
            self.addRow()
        self.setCalendarDate(QDate.fromString(timeStamp, 'dd.MM.yyyy').getDate())
        
        for row, rowData in enumerate(DataClasterComponent):
            self.table.cellWidget(row, 0).setCurrentIndex(rowData[0]['cell_0'])
            self.table.cellWidget(row, 1).children()[1].setText(rowData[1]['cell_1.1'])
            self.table.cellWidget(row, 1).children()[2].setCurrentIndex(rowData[1]['cell_1.2'])
        
            if len(rowData[1]) == 4:
                quantityEdit = QLineEdit('')
                quantityEdit.setValidator(QDoubleValidator())
                CurrencySelector = QComboBox()
                for idx, key in enumerate(self._Currency):
                    CurrencySelector.addItem(key)
                    CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
                    CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))

                self.table.cellWidget(row, 1).children()[0].addWidget(quantityEdit,50)
                self.table.cellWidget(row, 1).children()[0].addWidget(CurrencySelector,50)

                self.table.cellWidget(row, 1).children()[3].setText(rowData[1]['cell_1.3'])
                self.table.cellWidget(row, 1).children()[4].setCurrentIndex(rowData[1]['cell_1.4'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
#++++++++++++++++++++++++++ Accept ++++++++++++++++++++++++++++++++++++
    def acceptDialog(self):
        self.makeDataClaster()
        self._acceptState = True
        self.close()
#++++++++++++++++++++++++++ Reject ++++++++++++++++++++++++++++++++++++
    def rejectDialog(self):
        self._acceptState = False
        self.close()
#++++++++++++++++++ Get data claster part +++++++++++++++++++++++++++++
    def getDataClasterPart(self):
        return self._dataContainer, self._acceptState
#++++++++++++++++++ incomeCategoryFormater ++++++++++++++++++++++++++++
    def incomeCategoryFormater(self):
        changedSelectrorIndex = self.sender()
        self.rowNumb = self.table.rowCount()
        for  row in range (self.rowNumb):
            if self.table.cellWidget(row,0) == changedSelectrorIndex:
                if self.table.cellWidget(row,0).currentIndex() == 7:
                    if len(self.table.cellWidget(row, 1).children()[0]) == 2:
                        quantityEdit = QLineEdit('')
                        quantityEdit.setValidator(QDoubleValidator())
                        CurrencySelector = QComboBox()
                        for idx, key in enumerate(self._Currency):
                            CurrencySelector.addItem(key)
                            CurrencySelector.setItemData(idx, Qt.AlignCenter, Qt.TextAlignmentRole)
                            CurrencySelector.setItemIcon(idx, QtGui.QIcon(self._Currency[key]))

                        self.table.cellWidget(row, 1).children()[0].addWidget(quantityEdit,50)
                        self.table.cellWidget(row, 1).children()[0].addWidget(CurrencySelector,50)
                else:
                    try:
                        self.table.cellWidget(row, 1).children()[0].itemAt(2).widget().deleteLater()
                        self.table.cellWidget(row, 1).children()[0].itemAt(3).widget().deleteLater()
                    except AttributeError:
                        pass
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
    def read(self):
        return self._dataContainer
#+++++++++++++++++++++++++++ Test +++++++++++++++++++++++++++++++++++++
    def test(self):
        print("Test")
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

    _EventNames = ["პური", "იოგურტი", "ლობიო", "შაქარი", "კარტოფილი"]
    outcomeTable_header = ['მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
    incomeTable_header = ['წყარო','რაოდენობა']
    incomeSourceCategory = ['ავანსი','ხელფასი','პრემია','მივლინება','ქეშბექი','საჩუქარი','პრიზი','კონვერტაცია','სხვა','ვალი მიღება','სესხი']
    outComeCategory = [	'კვება','სხვადასხვა','ქირა','საყოფაცხოვრებო','კომუნალური','ტელეფონი',
                        'ინტერნეტი','გართობა','ტანსაცმელი','ჰიგიენა','მედიკამენტები','ინტერნეტი',
                        'ტრანსპორტი','მოწყობილობები','დასვენება','საჩუქარი','გამოწერა','საკომისიო','აღჭურვილობა',
                        'ვარჯიში','რემონტი','ექიმთან კონსულტაცია','მკურნალობა','ჯარიმა','მოგზაურობა','გასესხება','ვალის გადახდა']
    units = ['--','ც','კგ','გრ','ლ','მლ','კვტ','თვე','დღე']
    Currency = {'₽'  : 'icon/Ruble.png',
                '$'  : 'icon/Dollar.png',
                '€'  : 'icon/Euro.png',
                'CHF': 'icon/swiss-franc.png',
                '₾'  : 'icon/Lari.png',
                '¥'  : 'icon/yuan.png'}
    outcomeData =  {'22.01.1993': [[{'cell_0': 'პური'},
                                    {'cell_1.1': '2', 'cell_1.2': 1},
                                    {'cell_2.1': 0},
                                    {   'cell_3.1': '30',
                                        'cell_3.2': 1,
                                        'cell_3.3': '--',
                                        'cell_3.4': 0},
                                    {'cell_4': False}]],
                    '23.01.1993': [[{'cell_0': 'იოგურტი'},
                                    {'cell_1.1': '5', 'cell_1.2': 1},
                                    {'cell_2.1': 0},
                                    {   'cell_3.1': '30',
                                        'cell_3.2': 1,
                                        'cell_3.3': '100',
                                        'cell_3.4': 0},
                                    {'cell_4': False}],
                                [ {'cell_0': 'ლობიო'},
                                    {'cell_1.1': '1', 'cell_1.2': 2},
                                    {'cell_2.1': 0},
                                    {   'cell_3.1': '44',
                                        'cell_3.2': 3,
                                        'cell_3.3': '--',
                                        'cell_3.4': 0},
                                    {'cell_4': True}],
                                [ {'cell_0': 'წიწიბურა'},
                                    {'cell_1.1': '2', 'cell_1.2': 2},
                                    {'cell_2.1': 0},
                                    {   'cell_3.1': '64',
                                        'cell_3.2': 2,
                                        'cell_3.3': '54',
                                        'cell_3.4': 0},
                                    {'cell_4': False}]]}
    #Window = OutcomeEventClaster(outcomeTable_header, _EventNames, outComeCategory, units, Currency)
    #Window.EditDataClaster(outcomeData['23.01.1993'], '23.01.1993')

    incomeData =  {	'22.01.1993': [[{'cell_0': 7},
                                    {'cell_1.1': '100',
                                        'cell_1.2': 1,
                                        'cell_1.3': '16500',
                                        'cell_1.4': 0}],
                                    [{'cell_0': 7},
                                    {'cell_1.1': '150',
                                        'cell_1.2': 1,
                                        'cell_1.3': '25500',
                                        'cell_1.4': 0}]]}
    Window = IncomeEventClaster(incomeTable_header, incomeSourceCategory, Currency)
    Window.EditDataClaster(incomeData['22.01.1993'], '22.01.1993')
    sys.exit(App.exec_())