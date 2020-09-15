##!/usr/bin/python3
# -*- coding: utf-8 -*-
# ---------------------------- Libraries ------------------------------
from PyQt5.QtWidgets import (   QMainWindow, QApplication, 
                                QPlainTextEdit, QDateTimeEdit,
                                QFileDialog, QTableWidget, QLineEdit,
                                QSplitter, QHeaderView, QLabel,
                                QHeaderView, QPushButton, QWidget,
                                QAction, QTabWidget, QVBoxLayout,
                                QHBoxLayout, QDesktopWidget,
                                QCheckBox, QToolBox)
from PyQt5.QtGui import     (QIcon, QPalette, QLinearGradient,
                            QColor, QBrush, QPixmap)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt, QDir
from PyQt5 import QtGui, QtCore
from EventClasterTable import OutcomeEventClaster, IncomeEventClaster
from Plots import PlotCanvas, PlotCanvasPieChart, PlotCanvasHistogram
from DashBoardDisplays import DashBoardDisplay
from Table import OutcomeTable, IncomeTable
from CalendarDialog import CalendarDialog
from SettingsDialog import Settings
from datetime import datetime
from pprint import pprint, pformat
import json
import sys

class App(QMainWindow):
# ++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.selectedRangeDataOutcome = {}
        self.selectedRangeDataIncome = {}
        self.outcomeTable_header = ['დრო','მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
        self.incomeTable_header = ['დრო','წყარო','რაოდენობა']

        self.outcomeTable_headerFormat = ['მოვლენა','რაოდენობა','კატეგორია','ფასი','გადახდის ტიპი']
        self.incomeTable_headerFormat = ['წყარო','რაოდენობა']

        self.temp_data = {  'config': { 'language' : 'georgian',
                                        'length'   : 1800, 
                                        'width'    : 800},
                            'calendarRange' : {'start_date' : '12.02.2018',
                                               'stop_date'  : '22.02.2020'},
                            'outcomeTableData' : {},
                            'incomeTableData'  : {}}
        self._units = ['--','ც','კგ','გრ','ლ','მლ','კვტ','თვე','დღე','მ','სმ','მმ']
        self._incomeSourceCategory = ['ავანსი','ხელფასი','პრემია',
                                      'მივლინება','ქეშბექი','საჩუქარი','სხვა',
                                      'კონვერტაცია','სესხი','ვალის მიღება',
                                      'საწყისი კაპიტალი','ანაზღაურება','პენსია',
                                      'სოციალური დახმარება']
        self._outComeCategory = ['კვება','სხვადასხვა','ქირა','საყოფაცხოვრებო',
                                 'კომუნალური','ტელეფონი','ინტერნეტი',
                                 'გართობა','ტანსაცმელი','ჰიგიენა','მედიკამენტები',
                                 'ინტერნეტი','ტრანსპორტი','მოწყობილობები',
                                 'დასვენება','საჩუქარი','გამოწერა','საკომისიო',
                                 'აღჭურვილობა','ვარჯიში','რემონტი',
                                 'ექიმთან კონსულტაცია','მკურნალობა','ჯარიმა',
                                 'მოგზაურობა','გასესხება','სესხის დაბრუნება',
                                 'განათლება','თავის მოვლა','დაზღვევა',
                                 'ჯანდაცვა','საწვავი','სამედიცინო მომსახურება']
        self._currency = {	'₽'  : 'icon/Ruble.svg',
                            '$'  : 'icon/Dollar.svg',
                            '€'  : 'icon/Euro.svg',
                            'CHF': 'icon/swiss-franc.svg',
                            '₾'  : 'icon/Lari.svg',
                            '¥'  : 'icon/yuan.svg'}
        self._currencyIndex = {	0 : '₽',
                                1 : '$',
                                2 : '€',
                                3 : 'CHF',
                                4 : '₾',
                                5 : '¥'}
        self._eventNames = []
        self._filePath = ""
        self._tt = True
# ------------------------- Initialization ----------------------------
        self.initUI()
# +++++++++++++++++++++++++++++ initUI ++++++++++++++++++++++++++++++++
    def initUI(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('ფინანსების მართვა')
        self.setWindowIcon(QtGui.QIcon("icon/finance.svg"))
        self.setGeometry(0, 0, int(self.temp_data['config']['length']), int(self.temp_data['config']['width']))
        self.center()
# --------------------------- Create menu -----------------------------
        mainMenu = self.menuBar()
# --------------------------- Create tabs -----------------------------
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
# ----------------------- create menu options -------------------------
        fileMenu = mainMenu.addMenu('ფაილი')
        editMenu = mainMenu.addMenu('რედაქტირება')
        toolsMenu = mainMenu.addMenu('ინსტრუმენტები')
        viewMenu = mainMenu.addMenu('ინტერფეისი')
        toggleTool = QAction("ინსტრუმენტთა ველი", self, checkable=True)
        toggleTool.triggered.connect(self.handleToggleTool)

        viewMenu.addAction(toggleTool)
# ---------------------------- ToolBar --------------------------------
# ------------------------------ Exit ---------------------------------
        exitAct = QAction(QIcon('icon/close.svg'),'გასვლა', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(app.quit)
        fileMenu.addAction(exitAct)
# ------------------------------ new ----------------------------------
        newAct = QAction(QIcon('icon/new.svg'),'ახალი', self)
        newAct.setShortcut("Ctrl+N")
        fileMenu.addAction(newAct)
        newAct.triggered.connect(self.new)
# ------------------------------ open ---------------------------------
        openAct = QAction(QIcon('icon/open.svg'),'გახსნა', self)
        openAct.setShortcut("Ctrl+O")
        openAct.triggered.connect(self.openFile)
        fileMenu.addAction(openAct)
# ------------------------------ Save ---------------------------------
        saveAct = QAction(QIcon('icon/save.svg'),'შენახვა', self)
        saveAct.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAct)
        saveAct.triggered.connect(self.save)
# ---------------------------- Save as --------------------------------
        save_asAct = QAction(QIcon('icon/save_as.svg'), 'შენახვა როგორც', self)
        fileMenu.addAction(save_asAct)
        save_asAct.triggered.connect(self.saveAs)
# --------------------------- Add event -------------------------------
        addEventAct = QAction(QIcon('icon/addEvent.svg'), 'დამატება', self)
        editMenu.addAction(addEventAct)
        addEventAct.triggered.connect(self.addEvent)
# --------------------------- Edit event ------------------------------
        EditEventAct = QAction(QIcon('icon/EditEvent.svg'), 'რედაქტირება', self)
        editMenu.addAction(EditEventAct)
        EditEventAct.triggered.connect(self.editEvent)
# -------------------------- Remove event -----------------------------
        removeEventAct = QAction(QIcon('icon/RemoveEvent.svg'), 'წაშლა', self)
        editMenu.addAction(removeEventAct)
        removeEventAct.triggered.connect(self.removeEvent)
# ---------------------- Select calendar range ------------------------
        CalendarAct = QAction(QIcon('icon/calendar.svg'), 'კალენდარი', self)
        editMenu.addAction(CalendarAct)
        CalendarAct.triggered.connect(self.selectCalendarRange)
        self.statusBarMessage('კალენდარი')
# ---------------------------- Settings  ------------------------------
        settingsAct = QAction(QIcon('icon/setting.svg'), 'პარამეტრები', self)
        fileMenu.addAction(settingsAct)
        settingsAct.triggered.connect(self.settings)
 # ---------------------------------------------- Print data structure ----------------------------------------------
        printAct = QAction(QIcon('icon/print.png'), 'მონაცემთა დაბეჭვდა', self)
        printAct.triggered.connect(self.printData)
# ------------------------------ Test ---------------------------------
        testAct = QAction(QIcon('icon/test.png'), 'ტესტი', self)
        testAct.triggered.connect(self.test)
# --------------------- Add buttons on toolbar ------------------------
        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(exitAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(newAct)
        self.toolbar.addAction(openAct)
        self.toolbar.addAction(saveAct)
        self.toolbar.addAction(save_asAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(addEventAct)
        self.toolbar.addAction(EditEventAct)
        self.toolbar.addAction(removeEventAct)
        self.toolbar.addAction(testAct)
        self.toolbar.addAction(CalendarAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(settingsAct)

        self.addToolBarBreak()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.TopToolBarArea , self.toolbar)
# ------------------------- Add tab pages -----------------------------
# ---------------------------- Add tabs -------------------------------
        self.tabs.addTab(self.tab1, "საინფორმაციო დაფა")
        self.tabs.addTab(self.tab2, "ხარჯები")
        self.tabs.addTab(self.tab3, "შემოსავლები")
        self.tabs.addTab(self.tab4, "ტერმინალი")
        self.setCentralWidget(self.tabs)
# -------------------------- tab1 layouts -----------------------------
        self.VlayoutTab1 = QVBoxLayout()
        self.HlayoutTab1 = QHBoxLayout()
# -------------------------- tab2 layouts -----------------------------
        self.VlayoutTab2 = QVBoxLayout()
# -------------------------- tab3 layouts -----------------------------
        self.VlayoutTab3 = QVBoxLayout()
# -------------------------- tab4 layouts -----------------------------
        self.VlayoutTab4 = QVBoxLayout()
# -------------------------- Outcome table ----------------------------
        self.outcomeTable = OutcomeTable(self.outcomeTable_header,
                                         self._outComeCategory,
                                         self._units,
                                         self._currencyIndex)
        self.VlayoutTab2.addWidget(self.outcomeTable)
# -------------------------- Income table -----------------------------
        self.incomeTable = IncomeTable( self.incomeTable_header,
                                        self._incomeSourceCategory,
                                        self._currencyIndex)
        self.VlayoutTab3.addWidget(self.incomeTable)
# ------------------------------ Plot ---------------------------------
#------------------------ Dash board window 1 -------------------------
        toolbox_1_Vlayout_1 = QVBoxLayout()
        toolbox_1_Hlayout_1 = QHBoxLayout()

        toolbox_1_Vlayout_2 = QVBoxLayout()
        toolbox_1_Hlayout_2 = QHBoxLayout()

        toolbox_1_Vlayout_4 = QVBoxLayout()
        toolbox_1_Hlayout_4 = QHBoxLayout()

        toolbox_1_Vlayout_5 = QVBoxLayout()
        toolbox_1_Hlayout_5 = QHBoxLayout()

        toolbox_1_Vlayout_6 = QVBoxLayout()
        toolbox_1_Hlayout_6 = QHBoxLayout()
####################### Finance dynamics plot #########################
        toolbox_1_Widgets_1 = QWidget()
        self.Plot_financeDynamics = PlotCanvas(title='ფინანსური დინამიკა', ylabel = 'რუბლი')
        toolbox_1_Vlayout_1.addWidget(self.Plot_financeDynamics)
        toolbar_1 = NavigationToolbar(self.Plot_financeDynamics, self)
        #self.hideAxisValueCheckBox1 = QCheckBox()
        #self.hideAxisValueCheckBox1.stateChanged.connect(lambda : self.test3(self.hideAxisValueCheckBox1.isChecked()))
        #self.hideAxisValueLabel1 = QLabel("Y დამალვა")
        #toolbar_1.addWidget(self.hideAxisValueCheckBox1)
        #toolbar_1.addWidget(self.hideAxisValueLabel1)
        toolbox_1_Vlayout_1.addWidget(toolbar_1)
        toolbox_1_Widgets_1.setLayout(toolbox_1_Vlayout_1)
        DashBoardbox_1 = QToolBox()
        DashBoardbox_1.setStyleSheet("""
        QToolBox::tab {
                        color: #b1b1b1;
                        padding: 3px;
                        border: 1px transparent black;
                        background-color: #302F2F;
                        border: 1px solid #4A4949;
                        border-bottom: 1px transparent #302F2F;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                        border-color: #3d8ec9;
                      }""")
        DashBoardbox_1.addItem(toolbox_1_Widgets_1, "ფინანსური დინამიკა")
###################### Category analyses plot #########################
        toolbox_1_Widgets_2 = QWidget()
        self.plot2 = PlotCanvasPieChart()
        self.plot3 = PlotCanvasPieChart()
        toolbox_1_Hlayout_2.addWidget(self.plot2)
        toolbox_1_Hlayout_2.addWidget(self.plot3)
        toolbox_1_Vlayout_2.addLayout(toolbox_1_Hlayout_2)
        toolbox_1_Widgets_2.setLayout(toolbox_1_Vlayout_2)
        DashBoardbox_1.addItem(toolbox_1_Widgets_2, "კატეგორიათა ანალიზი")
######################### Statisticas plot ############################
        toolbox_1_Widgets_4 = QWidget()
        self.OutcomeStatistic = PlotCanvasHistogram("ხარჯების სტატისტიკა")
        self.IncomeStatistic = PlotCanvasHistogram("შემოსავლების სტატისტიკა")
        toolbox_1_Vlayout_4.addWidget(self.OutcomeStatistic)
        toolbox_1_Vlayout_5.addWidget(self.IncomeStatistic)
        toolbar_4 = NavigationToolbar(self.OutcomeStatistic, self)
        toolbar_5 = NavigationToolbar(self.IncomeStatistic, self)
        toolbox_1_Vlayout_4.addWidget(toolbar_4)
        toolbox_1_Vlayout_5.addWidget(toolbar_5)
        toolbox_1_Hlayout_4.addLayout(toolbox_1_Vlayout_4)
        toolbox_1_Hlayout_4.addLayout(toolbox_1_Vlayout_5)
        toolbox_1_Widgets_4.setLayout(toolbox_1_Hlayout_4)
        DashBoardbox_1.addItem(toolbox_1_Widgets_4, "სტატისტიკა")
#######################################################################
        toolbox_1_Widgets_6 = QWidget()
        self.plot6 = PlotCanvasHistogram('სტატისტიკა')
        toolbox_1_Vlayout_6.addWidget(self.plot6)
        toolbar_6 = NavigationToolbar(self.plot6, self)
        toolbox_1_Vlayout_6.addWidget(toolbar_6)
        toolbox_1_Widgets_6.setLayout(toolbox_1_Vlayout_6)
        DashBoardbox_1.addItem(toolbox_1_Widgets_6, "6")
#------------------------- Dash Board Box 2 ---------------------------
        DashBoardbox_2 = QToolBox()
        DashBoardbox_2.setStyleSheet("""
        QToolBox::tab {
                        color: #b1b1b1;
                        padding: 3px;
                        border: 1px transparent black;
                        background-color: #302F2F;
                        border: 1px solid #4A4949;
                        border-bottom: 1px transparent #302F2F;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                        border-color: #3d8ec9;
                      }""")
########################## Current currency ###########################
        self.CurrentCurrency = DashBoardDisplay()
        DashBoardbox_2.addItem(self.CurrentCurrency, "მიმდინარე ანგარიში")
############################ Full Income ##############################
        self.FullIncome = DashBoardDisplay()
        DashBoardbox_2.addItem(self.FullIncome, "შემოსავალი")
########################### Full OutIncome ############################
        self.FullOutcome = DashBoardDisplay()
        DashBoardbox_2.addItem(self.FullOutcome, "ხარჯი")
############################## To Lend ################################
        self.ToLend = DashBoardDisplay()
        DashBoardbox_2.addItem(self.ToLend, "გასესხებული")
############################# To Borrow ###############################
        self.ToBorrow = DashBoardDisplay()
        DashBoardbox_2.addItem(self.ToBorrow, "სესხი")
#######################################################################
        self.HlayoutTab1.addWidget(DashBoardbox_1,80)
        self.HlayoutTab1.addWidget(DashBoardbox_2,20)

        self.VlayoutTab1.addLayout(self.HlayoutTab1)
#----------------------------- Terminal -------------------------------
        self.terminal = QPlainTextEdit(self)
        self.VlayoutTab4.addWidget(self.terminal)
        #self.terminal.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(100,255,255,20); color: rgb(255,255,255);"
        #							"border-style: solid; border-radius: 8px; border-width: 3px; border-color: rgba(0,140,255,255);")
# ------------------------ Set tab 1 layout ---------------------------
        self.tab1.setLayout(self.VlayoutTab1)
# ------------------------ Set tab 2 layout ---------------------------
        self.tab2.setLayout(self.VlayoutTab2)
# ------------------------ Set tab 3 layout ---------------------------
        self.tab3.setLayout(self.VlayoutTab3)
# ------------------------ Set tab 4 layout ---------------------------
        self.tab4.setLayout(self.VlayoutTab4)
# +++++++++++++++++++++++++++++ center ++++++++++++++++++++++++++++++++
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
# ++++++++++++++++++++++++++++++ new ++++++++++++++++++++++++++++++++++
    def new(self):
        NewFilePath, _ = QFileDialog.getSaveFileName(self, 'ახალი ფაილი', QDir.homePath(), "JSON Files(*.json)")
        if NewFilePath != '':
            self._filePath = NewFilePath

            self.temp_data = {	'config': { 'language' : 'georgian',
                                            'length'   : 1500, 
                                            'width'    : 900},
                                'calendarRange' : { 'start_date' : '12.02.2018',
                                                    'stop_date'  : '22.02.2020'},
                                'outcomeTableData' : {},
                                'incomeTableData'  : {}}
            self.save()
            self.importData(self._filePath)
            if len(self.temp_data['outcomeTableData']) != 0:
                self.outcomeTable.importEvents(self.temp_data['outcomeTableData'])
                self.incomeTable.importEvents(self.temp_data['incomeTableData'])
            else:
                self.outcomeTable.setRowCount(0)
                self.incomeTable.setRowCount(0)
            self.statusBarMessage('ახალი')
# ++++++++++++++++++++++++++++++ open +++++++++++++++++++++++++++++++++
    def openFile(self):
        OpenfilePath, _ = QFileDialog.getOpenFileName(self, 'ფაილის გახსნა', QDir.currentPath(), "JSON Files(*.json)")
        if OpenfilePath != '':
            self._filePath = OpenfilePath
            self.importData(self._filePath)
            if len(self.temp_data['outcomeTableData']) != 0:
                self.temp_data['outcomeTableData'] = self.sortEventsDates(self.temp_data['outcomeTableData'])
                self.temp_data['incomeTableData'] = self.sortEventsDates(self.temp_data['incomeTableData'])

                self.loadSelectedDataOutcome()
                self.loadSelectedDataIncome()
                self.calculations()
# +++++++++++++++++++ load selected data Outcome ++++++++++++++++++++++
    def loadSelectedDataOutcome(self):
        self.selectedRangeDataOutcome = {}
        for date in self.temp_data['outcomeTableData'].keys():
            if datetime.strptime(date, "%d.%m.%Y") >= datetime.strptime(self.temp_data['calendarRange']['start_date'], "%d.%m.%Y") and datetime.strptime(date, "%d.%m.%Y") <= datetime.strptime(self.temp_data['calendarRange']['stop_date'], "%d.%m.%Y"):
                self.selectedRangeDataOutcome[date] = self.temp_data['outcomeTableData'][date]
        self.selectedRangeDataOutcome = self.sortEventsDates(self.selectedRangeDataOutcome)
        self.outcomeTable.importEvents(self.selectedRangeDataOutcome)
# +++++++++++++++++++ load selected data Income +++++++++++++++++++++++
    def loadSelectedDataIncome(self):
        self.selectedRangeDataIncome = {}
        for date in self.temp_data['incomeTableData'].keys():
            if datetime.strptime(date, "%d.%m.%Y") >= datetime.strptime(self.temp_data['calendarRange']['start_date'], "%d.%m.%Y") and datetime.strptime(date, "%d.%m.%Y") <= datetime.strptime(self.temp_data['calendarRange']['stop_date'], "%d.%m.%Y"):
                self.selectedRangeDataIncome[date] = self.temp_data['incomeTableData'][date]
        self.selectedRangeDataIncome = self.sortEventsDates(self.selectedRangeDataIncome)
        self.incomeTable.importEvents(self.selectedRangeDataIncome)
# ++++++++++++++++++++++++++++++ Save +++++++++++++++++++++++++++++++++
    def save(self):
        if self._filePath != '':
            with open(self._filePath, 'w') as outfile:
                json.dump(self.temp_data, outfile, indent=4)
            self.statusBarMessage('შენახვა')
# ++++++++++++++++++++++++++++ Save as ++++++++++++++++++++++++++++++++
    def saveAs(self):
        saveAspath, _ = QFileDialog.getSaveFileName(self, 'ფაილის შენახვა', QDir.homePath(), "JSON Files(*.json)")
        if saveAspath != '':
            self._filePath = saveAspath
            self.save()
            self.statusBarMessage('შენახვა როგორც')
# +++++++++++++++++++++++ Sort events dates +++++++++++++++++++++++++++
    def sortEventsDates(self, dateClasters):
        unsortedDates = [datetime.strptime(ts, "%d.%m.%Y") for ts in dateClasters.keys()]
        unsortedDates.sort()
        sorteddates = [datetime.strftime(ts, "%d.%m.%Y") for ts in unsortedDates]
        sortedDateClasters = {}
        for date in sorteddates:
            sortedDateClasters[date] = dateClasters[date]
        return sortedDateClasters
# +++++++++++++++++++++++++++ importData ++++++++++++++++++++++++++++++
    def importData(self, filePath):
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
# +++++++++++++++++++++ Print data structure ++++++++++++++++++++++++++
    def printData(self):
        self.term(" კონფიგურაცია ---> " + str(self.temp_data['config']))
        self.term(" კალენდარი start_date ---> " + str(self.temp_data['calendarRange']['start_date']))
        self.term(" კალენდარი stop_date ---> " + str(self.temp_data['calendarRange']['stop_date']))
        self.term(" ხარჯები ---> " + str(self.temp_data['outcomeTableData']))
        self.term(" შემოსავლები ---> " + str(self.temp_data['incomeTableData']))
        self.statusBarMessage("მონაცემთა დაბეჭვდა")
# +++++++++++++++++++++ Select calendar range +++++++++++++++++++++++++
    def selectCalendarRange(self):
        selectCalendarRangeDialog = CalendarDialog()
        selectCalendarRangeDialog.setCalendarRange(self.temp_data['calendarRange'])
        selectCalendarRangeDialog.exec_()
        dateRange, acceptState = selectCalendarRangeDialog.getRange()
        if acceptState == True:
            self.temp_data['calendarRange'] = dateRange
            print()
            self.loadSelectedDataOutcome()
            self.loadSelectedDataIncome()
            self.calculations()
# ++++++++++++++++++++++++++++ settings +++++++++++++++++++++++++++++++
    def settings(self):
        Settingsdialog = Settings(self.temp_data['config'])
        Settingsdialog.exec_()
        settings, acceptState = Settingsdialog.getSettings()
        if acceptState == True:
            self.temp_data['config'] = settings
            self.setGeometry(0, 0, int(self.temp_data['config']["length"]), int(self.temp_data['config']["width"]))
            self.center()
            self.statusBarMessage("პარამეტრები")
# +++++++++++++++++++++++++++ Add Event +++++++++++++++++++++++++++++++
    def addEvent(self):
        if self.tabs.currentIndex() == 1:
            self.addOutcomeEvent()
        elif self.tabs.currentIndex() == 2:
            self.addIncomeEvent()
        else:
            pass
# +++++++++++++++++++++++ Add Outcome Event +++++++++++++++++++++++++++
    def addOutcomeEvent(self):
        self.generateCompliterList()
        Outcomedialog = OutcomeEventClaster(self.outcomeTable_headerFormat,
                                            self._eventNames,
                                            self._outComeCategory,
                                            self._units,
                                            self._currency)
        Outcomedialog.exec_()
        newOutcomeEvent, acceptState = Outcomedialog.getDataClasterPart()
        if acceptState == True:
            self.temp_data['outcomeTableData'].update(newOutcomeEvent)
            self.temp_data['outcomeTableData'] = self.sortEventsDates(self.temp_data['outcomeTableData'])
            self.loadSelectedDataOutcome()
            self.calculations()
# ++++++++++++++++++++++++ Add Income Event +++++++++++++++++++++++++++
    def addIncomeEvent(self):
        Incomedialog = IncomeEventClaster(self.incomeTable_headerFormat,
                                          self._incomeSourceCategory,
                                          self._currency)
        Incomedialog.exec_()
        newIncomeEvent, acceptState = Incomedialog.getDataClasterPart()
        if acceptState == True:
            self.temp_data['incomeTableData'].update(newIncomeEvent)
            self.temp_data['incomeTableData'] = self.sortEventsDates(self.temp_data['incomeTableData'])
            self.loadSelectedDataIncome()
            self.calculations()
# +++++++++++++++++++++++++++ Edit Event ++++++++++++++++++++++++++++++
    def editEvent(self):
        if self.tabs.currentIndex() == 1:
            self.editOutcomeEvent()
        elif self.tabs.currentIndex() == 2:
            self.editIncomeEvent()
        else:
            pass
# +++++++++++++++++++++++ Edit Outcome Event ++++++++++++++++++++++++++
    def editOutcomeEvent(self):
        row = self.outcomeTable.currentRow()
        column = self.outcomeTable.currentColumn()
        try:
            selectedDate = self.outcomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
            self.generateCompliterList()
            Outcomedialog = OutcomeEventClaster(self.outcomeTable_headerFormat,
                                                self._eventNames,
                                                self._outComeCategory,
                                                self._units,
                                                self._currency)
            Outcomedialog.EditDataClaster(self.temp_data['outcomeTableData'][selectedDate], selectedDate)
            Outcomedialog.exec_()
            editedOutcomeEvent, acceptState = Outcomedialog.getDataClasterPart()
            if acceptState == True:
                if {selectedDate : self.temp_data['outcomeTableData'][selectedDate]}.keys() != editedOutcomeEvent.keys():
                    del self.temp_data['outcomeTableData'][selectedDate]
                self.temp_data['outcomeTableData'].update(editedOutcomeEvent)
                self.temp_data['outcomeTableData'] = self.sortEventsDates(self.temp_data['outcomeTableData'])
                self.loadSelectedDataOutcome()
                self.calculations()
        except AttributeError:
            pass
# ++++++++++++++++++++++ Edit Income Event ++++++++++++++++++++++++++++
    def editIncomeEvent(self):
        row = self.incomeTable.currentRow()
        column = self.incomeTable.currentColumn()
        try:
            selectedDate = self.incomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
            Incomedialog = IncomeEventClaster(self.incomeTable_headerFormat, self._incomeSourceCategory, self._currency)
            Incomedialog.EditDataClaster(self.temp_data['incomeTableData'][selectedDate], selectedDate)
            Incomedialog.exec_()
            editedIncomeEvent, acceptState = Incomedialog.getDataClasterPart()
            if acceptState == True:
                if {selectedDate : self.temp_data['incomeTableData'][selectedDate]}.keys() != editedIncomeEvent.keys():
                    del self.temp_data['incomeTableData'][selectedDate]
                self.temp_data['incomeTableData'].update(editedIncomeEvent)
                self.temp_data['incomeTableData'] = self.sortEventsDates(self.temp_data['incomeTableData'])
                self.loadSelectedDataIncome()
                self.calculations()
        except AttributeError:
            pass
# ++++++++++++++++++++++++++ Remove Event +++++++++++++++++++++++++++++
    def removeEvent(self):
        if self.tabs.currentIndex() == 1:
            self.removeOutcomeEvent()
        elif self.tabs.currentIndex() == 2:
            self.removeIncomeEvent()
        else:
            pass
# ++++++++++++++++++++++ Remove Outcome Event +++++++++++++++++++++++++
    def removeOutcomeEvent(self):
        row = self.outcomeTable.currentRow()
        column = self.outcomeTable.currentColumn()
        if column == 0:
            selectedDate = self.outcomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
            del self.temp_data['outcomeTableData'][selectedDate]
            self.loadSelectedDataOutcome()
            self.calculations()
# ++++++++++++++++++++++ Remove Income Event ++++++++++++++++++++++++++
    def removeIncomeEvent(self):
        row = self.incomeTable.currentRow()
        column = self.incomeTable.currentColumn()
        if column == 0:
            selectedDate = self.incomeTable.cellWidget(row,column).date().toString("dd.MM.yyyy")
            del self.temp_data['incomeTableData'][selectedDate]
            self.loadSelectedDataIncome()
            self.calculations()
# +++++++++++++++++++++++++ Terminal Print ++++++++++++++++++++++++++++
    def term(self, Text):
        self.terminal.insertPlainText("-----------------------------\n")
        self.terminal.insertPlainText("----> " + Text + "\n")
        self.terminal.insertPlainText("-----------------------------\n")
        self.statusBarMessage("ტერმინალში ბეჭვდა")
# +++++++++++++++++++++++ StatusBar Message +++++++++++++++++++++++++++
    def statusBarMessage(self, message):
        self.statusBar().showMessage(message)
# +++++++++++++++++++++++ Toolbar Hide-Show +++++++++++++++++++++++++++
    def handleToggleTool(self):
        if self._tt == True:
            self.toolbar.hide()
            self._tt = False
        else:
            self.toolbar.show()
            self._tt = True
# ++++++++++++++++++++ Generate compliter list ++++++++++++++++++++++++
    def generateCompliterList(self):
        for key in self.temp_data['outcomeTableData']:
            for item in self.temp_data['outcomeTableData'][key]:
                self._eventNames.append(item[0]['cell_0'])
        self._eventNames = list(dict.fromkeys(self._eventNames))
# +++++++++++++++++++++++++ Calculations ++++++++++++++++++++++++++++++
    def calculations(self):
        ######### To lend colector #########
        OutcomeSumRubleLend = 0
        OutcomeSumDollarLend = 0
        OutcomeSumEuroLend = 0
        OutcomeSumFrancLend = 0
        OutcomeSumLariLend = 0
        OutcomeSumYuanLend = 0
        ##### Outcome by card colector #####
        OutcomeSumRubleCard = 0
        OutcomeSumDollarCard = 0
        OutcomeSumEuroCard = 0
        OutcomeSumFrancCard = 0
        OutcomeSumLariCard = 0
        OutcomeSumYuanCard = 0
        ##### Outcome by cash colector #####
        OutcomeSumRubleCash = 0
        OutcomeSumDollarCash = 0
        OutcomeSumEuroCash = 0
        OutcomeSumFrancCash = 0
        OutcomeSumLariCash = 0
        OutcomeSumYuanCash = 0

        outcomeTimestamps_RubleTemp = {}
        outcomeTimestamps_DollarTemp = {}
        outcomeTimestamps_EuroTemp = {}
        outcomeTimestamps_FrancTemp = {}
        outcomeTimestamps_LariTemp = {}
        outcomeTimestamps_YuanTemp = {}

        outcomeTimestamps_Ruble = []
        outcomeDataDynamic_Ruble = []
        outcomeTimestamps_Dollar = []
        outcomeDataDynamic_Dollar = []
        outcomeTimestamps_Euro = []
        outcomeDataDynamic_Euro = []
        outcomeTimestamps_Franc = []
        outcomeDataDynamic_Franc = []
        outcomeTimestamps_Lari = []
        outcomeDataDynamic_Lari = []
        outcomeTimestamps_Yuan = []
        outcomeDataDynamic_Yuan = []

        for key in self.temp_data['outcomeTableData']:
            outcomeDynamic_Ruble = 0.
            outcomeDynamic_Dollar = 0.
            outcomeDynamic_Euro = 0.
            outcomeDynamic_Franc = 0.
            outcomeDynamic_Lari = 0.
            outcomeDynamic_Yuan = 0.
            for item in self.temp_data['outcomeTableData'][key]:
                ByCard_Ruble = 0.
                ByCash_Ruble = 0.
                ByCard_Dollar = 0.
                ByCash_Dollar = 0.
                ByCard_Euro = 0.
                ByCash_Euro = 0.
                ByCard_Franc = 0.
                ByCash_Franc = 0.
                ByCard_Lari = 0.
                ByCash_Lari = 0.
                ByCard_Yuan = 0.
                ByCash_Yuan = 0.
                ######### To lend calculator #########
                if item[2]['cell_2.1'] == 25:
                    if item[3]['cell_3.2'] == 0:
                        OutcomeSumRubleLend += float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 1:
                        OutcomeSumDollarLend += float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 2:
                        OutcomeSumEuroLend += float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 3:
                        OutcomeSumFrancLend += float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 4:
                        OutcomeSumLariLend += float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 5:
                        OutcomeSumYuanLend += float(item[3]['cell_3.1'])
                ######## Outcome calculator ##########
                if item[4]['cell_4'] == False:
                    if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                        if item[3]['cell_3.4'] == 0:
                            OutcomeSumRubleCard += float(item[3]['cell_3.3'])
                            ByCard_Ruble = float(item[3]['cell_3.3'])
                        elif item[3]['cell_3.4'] == 1:
                            OutcomeSumDollarCard += float(item[3]['cell_3.3'])
                            ByCard_Dollar = float(item[3]['cell_3.3'])
                        elif item[3]['cell_3.4'] == 2:
                            OutcomeSumEuroCard += float(item[3]['cell_3.3'])
                            ByCard_Euro = float(item[3]['cell_3.3'])
                        elif item[3]['cell_3.4'] == 3:
                            OutcomeSumFrancCard += float(item[3]['cell_3.3'])
                            ByCard_Franc = float(item[3]['cell_3.3'])
                        elif item[3]['cell_3.4'] == 4:
                            OutcomeSumLariCard += float(item[3]['cell_3.3'])
                            ByCard_Lari = float(item[3]['cell_3.3'])
                        elif item[3]['cell_3.4'] == 5:
                            OutcomeSumYuanCard += float(item[3]['cell_3.3'])
                            ByCard_Yuan = float(item[3]['cell_3.3'])
                    else:
                        if item[3]['cell_3.2'] == 0:
                            OutcomeSumRubleCard += float(item[3]['cell_3.1'])
                            ByCard_Ruble = float(item[3]['cell_3.1'])
                        elif item[3]['cell_3.2'] == 1:
                            OutcomeSumDollarCard += float(item[3]['cell_3.1'])
                            ByCard_Dollar = float(item[3]['cell_3.1'])
                        elif item[3]['cell_3.2'] == 2:
                            OutcomeSumEuroCard += float(item[3]['cell_3.1'])
                            ByCard_Euro = float(item[3]['cell_3.1'])
                        elif item[3]['cell_3.2'] == 3:
                            OutcomeSumFrancCard += float(item[3]['cell_3.1'])
                            ByCard_Franc = float(item[3]['cell_3.1'])
                        elif item[3]['cell_3.2'] == 4:
                            OutcomeSumLariCard += float(item[3]['cell_3.1'])
                            ByCard_Lari = float(item[3]['cell_3.1'])
                        elif item[3]['cell_3.2'] == 5:
                            OutcomeSumYuanCard += float(item[3]['cell_3.1'])
                            ByCard_Yuan = float(item[3]['cell_3.1'])
                else:
                    if item[3]['cell_3.2'] == 0:
                        OutcomeSumRubleCash += float(item[3]['cell_3.1'])
                        ByCash_Ruble = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 1:
                        OutcomeSumDollarCash += float(item[3]['cell_3.1'])
                        ByCash_Dollar = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 2:
                        OutcomeSumEuroCash += float(item[3]['cell_3.1'])
                        ByCash_Euro = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 3:
                        OutcomeSumFrancCash += float(item[3]['cell_3.1'])
                        ByCash_Franc = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 4:
                        OutcomeSumLariCash += float(item[3]['cell_3.1'])
                        ByCash_Lari = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 5:
                        OutcomeSumYuanCash += float(item[3]['cell_3.1'])
                        ByCash_Yuan = float(item[3]['cell_3.1'])

                outcomeDynamic_Ruble += ByCard_Ruble + ByCash_Ruble
                outcomeDynamic_Dollar += ByCard_Dollar + ByCash_Dollar
                outcomeDynamic_Euro += ByCard_Euro + ByCash_Euro
                outcomeDynamic_Franc += ByCard_Franc + ByCash_Franc
                outcomeDynamic_Lari += ByCard_Lari + ByCash_Lari
                outcomeDynamic_Yuan += ByCard_Yuan + ByCash_Yuan

            if outcomeDynamic_Ruble != 0:
                outcomeTimestamps_RubleTemp[key] = round(-1*outcomeDynamic_Ruble,2)
                outcomeTimestamps_Ruble.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Ruble.append(round(-1*outcomeDynamic_Ruble,2))
            if outcomeDynamic_Dollar != 0:
                outcomeTimestamps_DollarTemp[key] = round(-1*outcomeDynamic_Dollar,2)
                outcomeTimestamps_Dollar.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Dollar.append(round(-1*outcomeDynamic_Dollar,2))
            if outcomeDynamic_Euro != 0:
                outcomeTimestamps_EuroTemp[key] = round(-1*outcomeDynamic_Euro,2)
                outcomeTimestamps_Euro.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Euro.append(round(-1*outcomeDynamic_Euro,2))
            if outcomeDynamic_Franc != 0:
                outcomeTimestamps_FrancTemp[key] = round(-1*outcomeDynamic_Franc,2)
                outcomeTimestamps_Franc.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Franc.append(round(-1*outcomeDynamic_Franc,2))
            if outcomeDynamic_Lari != 0:
                outcomeTimestamps_LariTemp[key] = round(-1*outcomeDynamic_Lari,2)
                outcomeTimestamps_Lari.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Lari.append(round(-1*outcomeDynamic_Lari,2))
            if outcomeDynamic_Yuan != 0:
                outcomeTimestamps_YuanTemp[key] = round(-1*outcomeDynamic_Yuan,2)
                outcomeTimestamps_Yuan.append(datetime.strptime(key, "%d.%m.%Y"))
                outcomeDataDynamic_Yuan.append(round(-1*outcomeDynamic_Yuan,2))
        ######### To lend display #########
        self.ToLend.updateDisplay([	OutcomeSumRubleLend,
                                    OutcomeSumDollarLend,
                                    OutcomeSumEuroLend,
                                    OutcomeSumFrancLend,
                                    OutcomeSumLariLend,
                                    OutcomeSumYuanLend])

        OutcomeRuble = round(OutcomeSumRubleCard + OutcomeSumRubleCash,2)
        OutcomeDollar = round(OutcomeSumDollarCard + OutcomeSumDollarCash,2)
        OutcomeEuro = round(OutcomeSumEuroCard + OutcomeSumEuroCash,2)
        OutcomeFranc = round(OutcomeSumFrancCard + OutcomeSumFrancCash,2)
        OutcomeLari = round(OutcomeSumLariCard + OutcomeSumLariCash,2)
        OutcomeYuan = round(OutcomeSumYuanCard + OutcomeSumYuanCash,2)
        ######### Outcome display #########
        self.FullOutcome.updateDisplay([OutcomeRuble,
                                        OutcomeDollar,
                                        OutcomeEuro,
                                        OutcomeFranc,
                                        OutcomeLari,
                                        OutcomeYuan])
        ####################################
        ###### To borrow container #########
        TakeCredit_Ruble = 0
        TakeCredit_Dollar = 0
        TakeCredit_Euro = 0
        TakeCredit_Franc = 0
        TakeCredit_Lari = 0
        TakeCredit_Yuan = 0
        ######## income container ##########
        IncomeSumRuble = 0
        IncomeSumDollar = 0
        IncomeSumEuro = 0
        IncomeSumFranc = 0
        IncomeSumLari = 0
        IncomeSumYuan = 0
        ## To convert curency container ####
        ToConvert_Ruble = 0
        ToConvert_Dollar = 0
        ToConvert_Euro = 0
        ToConvert_Franc = 0
        ToConvert_Lari = 0
        ToConvert_Yuan = 0
        ### converted curency container ####
        Converted_Ruble = 0
        Converted_Dollar = 0
        Converted_Euro = 0
        Converted_Franc = 0
        Converted_Lari = 0
        Converted_Yuan = 0

        incomeTimestamps_RubleTemp = {}
        incomeTimestamps_DollarTemp = {}
        incomeTimestamps_EuroTemp = {}
        incomeTimestamps_FrancTemp = {}
        incomeTimestamps_LariTemp = {}
        incomeTimestamps_YuanTemp = {}


        incomeTimestamps_Ruble = []
        incomeDataDynamic_Ruble = []
        incomeTimestamps_Dollar = []
        incomeDataDynamic_Dollar = []
        incomeTimestamps_Euro = []
        incomeDataDynamic_Euro = []
        incomeTimestamps_Franc = []
        incomeDataDynamic_Franc = []
        incomeTimestamps_Lari = []
        incomeDataDynamic_Lari = []
        incomeTimestamps_Yuan = []
        incomeDataDynamic_Yuan = []

        for key in self.temp_data['incomeTableData']:
            incomeDynamic_Ruble = 0.
            incomeDynamic_Dollar = 0.
            incomeDynamic_Euro = 0.
            incomeDynamic_Franc = 0.
            incomeDynamic_Lari = 0.
            incomeDynamic_Yuan = 0.
            for item in self.temp_data['incomeTableData'][key]:
                ####### To borrow calculator #######
                if item[0]['cell_0'] == 8:
                    if item[1]['cell_1.2'] == 0:
                        TakeCredit_Ruble += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 1:
                        TakeCredit_Dollar += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 2:
                        TakeCredit_Euro += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 3:
                        TakeCredit_Franc += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 4:
                        TakeCredit_Lari += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 5:
                        TakeCredit_Yuan += float(item[1]['cell_1.1'])
                ######## Income calculator #########
                if len(item[1]) == 2:
                    if item[1]['cell_1.2'] == 0:
                        IncomeSumRuble += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 1:
                        IncomeSumDollar += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 2:
                        IncomeSumEuro += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 3:
                        IncomeSumFranc += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 4:
                        IncomeSumLari += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 5:
                        IncomeSumYuan += float(item[1]['cell_1.1'])
                ##### Own transfer calculator ######
                if len(item[1]) == 4:
                    if item[1]['cell_1.2'] == 0:
                        ToConvert_Ruble += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 1:
                        ToConvert_Dollar += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 2:
                        ToConvert_Euro += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 3:
                        ToConvert_Franc += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 4:
                        ToConvert_Lari += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 5:
                        ToConvert_Yuan += float(item[1]['cell_1.1'])
                if len(item[1]) == 4:
                    if item[1]['cell_1.4'] == 0:
                        Converted_Ruble += float(item[1]['cell_1.3'])
                    elif item[1]['cell_1.4'] == 1:
                        Converted_Dollar += float(item[1]['cell_1.3'])
                    elif item[1]['cell_1.4'] == 2:
                        Converted_Euro += float(item[1]['cell_1.3'])
                    elif item[1]['cell_1.4'] == 3:
                        Converted_Franc += float(item[1]['cell_1.3'])
                    elif item[1]['cell_1.4'] == 4:
                        Converted_Lari += float(item[1]['cell_1.3'])
                    elif item[1]['cell_1.4'] == 5:
                        Converted_Yuan += float(item[1]['cell_1.3'])
                ##### Own transfer calculator ######
                if item[0]['cell_0'] != 7:
                    if item[1]['cell_1.2'] == 0:
                        incomeDynamic_Ruble += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 1:
                        incomeDynamic_Dollar += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 2:
                        incomeDynamic_Euro += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 3:
                        incomeDynamic_Franc += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 4:
                        incomeDynamic_Lari += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 5:
                        incomeDynamic_Yuan += float(item[1]['cell_1.1'])
                else:
                    if item[1]['cell_1.2'] == 0:
                        incomeDynamic_Ruble -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 0:
                        incomeDynamic_Ruble += float(item[1]['cell_1.3'])

                    if item[1]['cell_1.2'] == 1:
                        incomeDynamic_Dollar -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 1:
                        incomeDynamic_Dollar += float(item[1]['cell_1.3'])

                    if item[1]['cell_1.2'] == 2:
                        incomeDynamic_Euro -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 2:
                        incomeDynamic_Euro += float(item[1]['cell_1.3'])

                    if item[1]['cell_1.2'] == 3:
                        incomeDynamic_Franc -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 3:
                        incomeDynamic_Franc += float(item[1]['cell_1.3'])

                    if item[1]['cell_1.2'] == 4:
                        incomeDynamic_Lari -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 4:
                        incomeDynamic_Lari += float(item[1]['cell_1.3'])

                    if item[1]['cell_1.2'] == 5:
                        incomeDynamic_Yuan -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 5:
                        incomeDynamic_Yuan += float(item[1]['cell_1.3'])

            if incomeDynamic_Ruble != 0:
                incomeTimestamps_Ruble.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Ruble.append(round(incomeDynamic_Ruble,2))
                incomeTimestamps_RubleTemp[key] = round(incomeDynamic_Ruble,2)
            if incomeDynamic_Dollar != 0:
                incomeTimestamps_Dollar.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Dollar.append(round(incomeDynamic_Dollar,2))
                incomeTimestamps_DollarTemp[key] = round(incomeDynamic_Dollar,2)
            if incomeDynamic_Euro != 0:
                incomeTimestamps_Euro.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Euro.append(round(incomeDynamic_Euro,2))
                incomeTimestamps_EuroTemp[key] = round(incomeDynamic_Euro,2)
            if incomeDynamic_Franc != 0:
                incomeTimestamps_Franc.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Franc.append(round(incomeDynamic_Franc,2))
                incomeTimestamps_FrancTemp[key] = round(incomeDynamic_Franc,2)
            if incomeDynamic_Lari != 0:
                incomeTimestamps_Lari.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Lari.append(round(incomeDynamic_Lari,2))
                incomeTimestamps_LariTemp[key] = round(incomeDynamic_Lari,2)
            if incomeDynamic_Yuan != 0:
                incomeTimestamps_Yuan.append(datetime.strptime(key, "%d.%m.%Y"))
                incomeDataDynamic_Yuan.append(round(incomeDynamic_Yuan,2))
                incomeTimestamps_YuanTemp[key] = round(incomeDynamic_Yuan,2)
#######################################################################
        DynamicGraphContainer_Ruble = self.eventMerging(incomeTimestamps_RubleTemp, outcomeTimestamps_RubleTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Ruble.append(incomeTimestamps_Ruble)
        DynamicGraphContainer_Ruble.append(incomeDataDynamic_Ruble)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Ruble.append(outcomeTimestamps_Ruble)
        DynamicGraphContainer_Ruble.append(outcomeDataDynamic_Ruble)
        ###########################################################
        DynamicGraphContainer_Dollar = self.eventMerging(incomeTimestamps_DollarTemp, outcomeTimestamps_DollarTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Dollar.append(incomeTimestamps_Dollar)
        DynamicGraphContainer_Dollar.append(incomeDataDynamic_Dollar)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Dollar.append(outcomeTimestamps_Dollar)
        DynamicGraphContainer_Dollar.append(outcomeDataDynamic_Dollar)
        ###########################################################
        DynamicGraphContainer_Euro = self.eventMerging(incomeTimestamps_EuroTemp, outcomeTimestamps_EuroTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Euro.append(incomeTimestamps_Euro)
        DynamicGraphContainer_Euro.append(incomeDataDynamic_Euro)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Euro.append(outcomeTimestamps_Euro)
        DynamicGraphContainer_Euro.append(outcomeDataDynamic_Euro)
        ###########################################################
        DynamicGraphContainer_Franc = self.eventMerging(incomeTimestamps_FrancTemp, outcomeTimestamps_FrancTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Franc.append(incomeTimestamps_Franc)
        DynamicGraphContainer_Franc.append(incomeDataDynamic_Franc)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Franc.append(outcomeTimestamps_Franc)
        DynamicGraphContainer_Franc.append(outcomeDataDynamic_Franc)
        ###########################################################
        DynamicGraphContainer_Lari = self.eventMerging(incomeTimestamps_LariTemp, outcomeTimestamps_LariTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Lari.append(incomeTimestamps_Lari)
        DynamicGraphContainer_Lari.append(incomeDataDynamic_Lari)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Lari.append(outcomeTimestamps_Lari)
        DynamicGraphContainer_Lari.append(outcomeDataDynamic_Lari)
        ###########################################################
        DynamicGraphContainer_Yuan = self.eventMerging(incomeTimestamps_YuanTemp, outcomeTimestamps_YuanTemp)
        ## Income Dynamic ##
        DynamicGraphContainer_Yuan.append(incomeTimestamps_Yuan)
        DynamicGraphContainer_Yuan.append(incomeDataDynamic_Yuan)
        ## Outcome Dynamic ##
        DynamicGraphContainer_Yuan.append(outcomeTimestamps_Yuan)
        DynamicGraphContainer_Yuan.append(outcomeDataDynamic_Yuan)


        self.Plot_financeDynamics.plot(DynamicGraphContainer_Ruble)

        #self.Plot_financeDynamics.plot(DynamicGraphContainer_Dollar)
        #self.Plot_financeDynamics.plot(DynamicGraphContainer_Euro)
        #self.Plot_financeDynamics.plot(DynamicGraphContainer_Franc)
        #self.Plot_financeDynamics.plot(DynamicGraphContainer_Lari)
        #self.Plot_financeDynamics.plot(DynamicGraphContainer_Yuan)

        incomedataArray_Ruble = []
        incomedataArray_Dollar = []
        incomedataArray_Euro = []
        incomedataArray_Franc = []
        incomedataArray_Lari = []
        incomedataArray_Yuan = []
        for key in self.temp_data['incomeTableData']:
            incomeDynamic_Ruble = 0.
            incomeDynamic_Dollar = 0.
            incomeDynamic_Euro = 0.
            incomeDynamic_Franc = 0.
            incomeDynamic_Lari = 0.
            incomeDynamic_Yuan = 0.
            for item in self.temp_data['incomeTableData'][key]:
                if item[0]['cell_0'] != 7:
                    if item[1]['cell_1.2'] == 0:
                        incomeDynamic_Ruble += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 1:
                        incomeDynamic_Dollar += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 2:
                        incomeDynamic_Euro += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 3:
                        incomeDynamic_Franc += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 4:
                        incomeDynamic_Lari += float(item[1]['cell_1.1'])
                    elif item[1]['cell_1.2'] == 5:
                        incomeDynamic_Yuan += float(item[1]['cell_1.1'])
                else:
                    if item[1]['cell_1.2'] == 0:
                        incomeDynamic_Ruble -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 0:
                        incomeDynamic_Ruble += float(item[1]['cell_1.3'])
                    if item[1]['cell_1.2'] == 1:
                        incomeDynamic_Dollar -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 1:
                        incomeDynamic_Dollar += float(item[1]['cell_1.3'])
                    if item[1]['cell_1.2'] == 2:
                        incomeDynamic_Euro -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 2:
                        incomeDynamic_Euro += float(item[1]['cell_1.3'])
                    if item[1]['cell_1.2'] == 3:
                        incomeDynamic_Franc -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 3:
                        incomeDynamic_Franc += float(item[1]['cell_1.3'])
                    if item[1]['cell_1.2'] == 4:
                        incomeDynamic_Lari -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 4:
                        incomeDynamic_Lari += float(item[1]['cell_1.3'])
                    if item[1]['cell_1.2'] == 5:
                        incomeDynamic_Yuan -= float(item[1]['cell_1.1'])
                    if item[1]['cell_1.4'] == 6:
                        incomeDynamic_Yuan += float(item[1]['cell_1.3'])

            if incomeDynamic_Ruble != 0:
                incomedataArray_Ruble.append(round(incomeDynamic_Ruble,2))
            if incomeDynamic_Dollar != 0:
                incomedataArray_Dollar.append(round(incomeDynamic_Dollar,2))
            if incomeDynamic_Euro != 0:
                incomedataArray_Euro.append(round(incomeDynamic_Euro,2))
            if incomeDynamic_Franc != 0:
                incomedataArray_Franc.append(round(incomeDynamic_Franc,2))
            if incomeDynamic_Lari != 0:
                incomedataArray_Lari.append(round(incomeDynamic_Lari,2))
            if incomeDynamic_Yuan != 0:
                incomedataArray_Yuan.append(round(incomeDynamic_Yuan,2))

        self.IncomeStatistic.updateHist(incomedataArray_Ruble)


        outcomedataArrayPerEvent_Ruble = []
        outcomedataArrayPerEvent_Dollar = []
        outcomedataArrayPerEvent_Euro = []
        outcomedataArrayPerEvent_Franc = []
        outcomedataArrayPerEvent_Lari = []
        outcomedataArrayPerEvent_Yuan = []
        for key in self.temp_data['outcomeTableData']:
            outcomeDynamic_Ruble = 0.
            outcomeDynamic_Dollar = 0.
            outcomeDynamic_Euro = 0.
            outcomeDynamic_Franc = 0.
            outcomeDynamic_Lari = 0.
            outcomeDynamic_Yuan = 0.
            for item in self.temp_data['outcomeTableData'][key]:
                ByCard_Ruble = 0.
                ByCash_Ruble = 0.
                ByCard_Dollar = 0.
                ByCash_Dollar = 0.
                ByCard_Euro = 0.
                ByCash_Euro = 0.
                ByCard_Franc = 0.
                ByCash_Franc = 0.
                ByCard_Lari = 0.
                ByCash_Lari = 0.
                ByCard_Yuan = 0.
                ByCash_Yuan = 0.
                if item[4]['cell_4'] == False:
                    if item[3]['cell_3.4'] == 0:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Ruble = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Ruble = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.4'] == 1:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Dollar = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Dollar = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.4'] == 2:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Euro = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Euro = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.4'] == 3:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Franc = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Franc = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.4'] == 4:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Lari = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Lari = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.4'] == 5:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Yuan = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Yuan = float(item[3]['cell_3.1'])
                else:
                    if item[3]['cell_3.2'] == 0:
                        ByCash_Ruble = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 1:
                        ByCash_Dollar = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 2:
                        ByCash_Euro = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 3:
                        ByCash_Franc = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 4:
                        ByCash_Lari = float(item[3]['cell_3.1'])
                    elif item[3]['cell_3.2'] == 5:
                        ByCash_Yuan = float(item[3]['cell_3.1'])

                outcomeDynamic_Ruble += ByCard_Ruble + ByCash_Ruble
                outcomeDynamic_Dollar += ByCard_Dollar + ByCash_Dollar
                outcomeDynamic_Euro += ByCard_Euro + ByCash_Euro
                outcomeDynamic_Franc += ByCard_Franc + ByCash_Franc
                outcomeDynamic_Lari += ByCard_Lari + ByCash_Lari
                outcomeDynamic_Yuan += ByCard_Yuan + ByCash_Yuan

            if outcomeDynamic_Ruble != 0:
                outcomedataArrayPerEvent_Ruble.append(round(outcomeDynamic_Ruble,2))
            if outcomeDynamic_Dollar != 0:
                outcomedataArrayPerEvent_Dollar.append(round(outcomeDynamic_Dollar,2))
            if outcomeDynamic_Euro != 0:
                outcomedataArrayPerEvent_Euro.append(round(outcomeDynamic_Euro,2))
            if outcomeDynamic_Franc != 0:
                outcomedataArrayPerEvent_Franc.append(round(outcomeDynamic_Franc,2))
            if outcomeDynamic_Lari != 0:
                outcomedataArrayPerEvent_Lari.append(round(outcomeDynamic_Lari,2))
            if outcomeDynamic_Yuan != 0:
                outcomedataArrayPerEvent_Yuan.append(round(outcomeDynamic_Yuan,2))

        #self.OutcomeStatistic.setXlabel("რუბლი")
        self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Ruble)

        #self.OutcomeStatistic.setXlabel("დოლარი")
        #self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Dollar)

        #self.OutcomeStatistic.setXlabel("ეურო")
        #self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Euro)

        #self.OutcomeStatistic.setXlabel("ფრანკი")
        #self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Franc)

        #self.OutcomeStatistic.setXlabel("ლარი")
        #self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Lari)

        #self.OutcomeStatistic.setXlabel("იუენი")
        #self.OutcomeStatistic.updateHist(outcomedataArrayPerEvent_Yuan)

        self.ToBorrow.updateDisplay([TakeCredit_Ruble,
                                    TakeCredit_Dollar,
                                    TakeCredit_Euro,
                                    TakeCredit_Franc,
                                    TakeCredit_Lari,
                                    TakeCredit_Yuan])
############################ Full Income ##############################
        IncomeRuble = round(IncomeSumRuble - ToConvert_Ruble + Converted_Ruble,2)
        IncomeDollar = round(IncomeSumDollar - ToConvert_Dollar + Converted_Dollar,2)
        IncomeEuro = round(IncomeSumEuro - ToConvert_Euro + Converted_Euro,2)
        IncomeFranc = round(IncomeSumFranc - ToConvert_Franc + Converted_Franc,2)
        IncomeLari = round(IncomeSumLari - ToConvert_Lari + Converted_Lari,2)
        IncomeYuan = round(IncomeSumYuan - ToConvert_Yuan + Converted_Yuan,2)

        self.FullIncome.updateDisplay([	IncomeRuble,
                                        IncomeDollar,
                                        IncomeEuro,
                                        IncomeFranc,
                                        IncomeLari,
                                        IncomeYuan])
######################### Current curencies ###########################
        Current_Ruble = round(IncomeRuble - OutcomeRuble,2)
        Current_Dollar = round(IncomeDollar - OutcomeDollar,2)
        Current_Euro = round(IncomeEuro - OutcomeEuro,2)
        Current_Franc = round(IncomeFranc - OutcomeFranc,2)
        Current_Lari = round(IncomeLari - OutcomeLari,2)
        Current_Yuan = round(IncomeYuan - OutcomeYuan,2)

        self.CurrentCurrency.updateDisplay([Current_Ruble,
                                            Current_Dollar,
                                            Current_Euro,
                                            Current_Franc,
                                            Current_Lari,
                                            Current_Yuan])
########################### Full Outcome ##############################
# ++++++++++++++++++++++++ Event merging ++++++++++++++++++++++++++++++
    def eventMerging(self,incomeContainer, outcomeContainer):
        #### merge income and outcome events #####
        temp = {}
        currentRuble = 0
        incomeTimestampsMirror = incomeContainer.copy()
        outcomeTimestampsMirror = outcomeContainer.copy()
        for incomedate in incomeContainer:
            currentRuble = incomeContainer[incomedate]
            if incomedate in outcomeContainer:
                currentRuble += outcomeContainer[incomedate]
                outcomeTimestampsMirror.pop(incomedate, None)
                incomeTimestampsMirror.pop(incomedate, None)
                temp.update({incomedate : currentRuble})

        dataContainer = {}
        dataContainer.update(temp)
        dataContainer.update(incomeTimestampsMirror)
        dataContainer.update(outcomeTimestampsMirror)
        ### sort merger events ####
        dataContainer = self.sortEventsDates(dataContainer)

        DynamicGraphTimeStamps = []
        DynamicGraphValues = []
        currentRuble = 0
        for dateTimeStamp in dataContainer:
            DynamicGraphTimeStamps.append(datetime.strptime(dateTimeStamp, "%d.%m.%Y"))
            currentRuble = currentRuble + dataContainer[dateTimeStamp]
            DynamicGraphValues.append(currentRuble)
        ## Finance Dynamic ##
        DynamicGraphContainer = []
        DynamicGraphContainer.append(DynamicGraphTimeStamps)
        DynamicGraphContainer.append(DynamicGraphValues)
        return DynamicGraphContainer

# +++++++++++++++++++++++++++++ Test ++++++++++++++++++++++++++++++++++
    def test(self):
        outcomeCategory1_Ruble = 0.
        outcomeCategory2_Ruble = 0.
        outcomeCategory3_Ruble = 0.
        outcomeCategory4_Ruble = 0.
        outcomeCategory5_Ruble = 0.
        outcomeCategory6_Ruble = 0.
        outcomeCategory7_Ruble = 0.
        outcomeCategory8_Ruble = 0.
        outcomeCategory9_Ruble = 0.
        outcomeCategory10_Ruble = 0.

        for key in self.temp_data['outcomeTableData']:
            for item in self.temp_data['outcomeTableData'][key]:
                ByCard_Ruble = 0.
                ByCash_Ruble = 0.
                if item[4]['cell_4'] == False:
                    if item[3]['cell_3.4'] == 0:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Ruble = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Ruble = float(item[3]['cell_3.1'])
                else:
                    if item[3]['cell_3.2'] == 0:
                        ByCash_Ruble = float(item[3]['cell_3.1'])

                if item[2]['cell_2.1'] == 0:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble

                    if outcomeTmp_Ruble != 0:
                        outcomeCategory1_Ruble = outcomeCategory1_Ruble + outcomeTmp_Ruble
                
                if item[2]['cell_2.1'] == 1:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory2_Ruble = outcomeCategory2_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 2:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory3_Ruble = outcomeCategory3_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 3:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory4_Ruble = outcomeCategory4_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 4:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory5_Ruble = outcomeCategory5_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 5:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory6_Ruble = outcomeCategory6_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 6:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory7_Ruble = outcomeCategory7_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 7:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory8_Ruble = outcomeCategory8_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 8:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory9_Ruble = outcomeCategory9_Ruble + outcomeTmp_Ruble
                if item[2]['cell_2.1'] == 9:
                    outcomeTmp_Ruble = ByCard_Ruble + ByCash_Ruble
                    if outcomeTmp_Ruble != 0:
                        outcomeCategory10_Ruble = outcomeCategory10_Ruble + outcomeTmp_Ruble
        #print(outcomeCategory1_Ruble)

        dataArray = []
        for key in self.temp_data['outcomeTableData']:
            for item in self.temp_data['outcomeTableData'][key]:
                ByCard_Ruble = 0.
                ByCash_Ruble = 0.
                if item[4]['cell_4'] == False:
                    if item[3]['cell_3.4'] == 0:
                        if item[3]['cell_3.3'] != '--' and item[3]['cell_3.3'] != '':
                            ByCard_Ruble = float(item[3]['cell_3.3'])
                        else:
                            ByCard_Ruble = float(item[3]['cell_3.1'])
                else:
                    if item[3]['cell_3.2'] == 0:
                        ByCash_Ruble = float(item[3]['cell_3.1'])
                if (ByCard_Ruble + ByCash_Ruble) != 0:
                    dataArray.append(ByCard_Ruble + ByCash_Ruble)
        #print(dataArray)
        self.OutcomeStatistic.updateHist(dataArray)

        labelsArray = []
        dataArray = []

        labelsArray.append(self._outComeCategory[0])
        labelsArray.append(self._outComeCategory[1])
        labelsArray.append(self._outComeCategory[2])
        labelsArray.append(self._outComeCategory[3])
        labelsArray.append(self._outComeCategory[4])
        labelsArray.append(self._outComeCategory[5])
        labelsArray.append(self._outComeCategory[6])
        labelsArray.append(self._outComeCategory[7])
        labelsArray.append(self._outComeCategory[8])
        labelsArray.append(self._outComeCategory[9])
        labelsArray.append(self._outComeCategory[10])

        dataArray.append(outcomeCategory1_Ruble)
        dataArray.append(outcomeCategory2_Ruble)
        dataArray.append(outcomeCategory3_Ruble)
        dataArray.append(outcomeCategory4_Ruble)
        dataArray.append(outcomeCategory5_Ruble)
        dataArray.append(outcomeCategory6_Ruble)
        dataArray.append(outcomeCategory7_Ruble)
        dataArray.append(outcomeCategory8_Ruble)
        dataArray.append(outcomeCategory9_Ruble)
        dataArray.append(outcomeCategory10_Ruble)

        self.plot2.updateChart(labelsArray, dataArray)

            #if outcomeDynamic_Ruble != 0:
            #	outcomeTimestamps_Ruble.append(datetime.strptime(key, "%d.%m.%Y"))
            #	outcomeDataDynamic_Ruble.append(round(-1*outcomeDynamic_Ruble,2))

        #self.term(pformat(outcomeDataDynamic_Ruble, indent=4) + '₽')
        self.statusBarMessage('ტესტი1')
#######################################################################
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

####### Note #######
## I should write a docstring for every class
# empty calculation data conteiner for graph bug
# correct data with cash paied content