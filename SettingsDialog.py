from PyQt5.QtWidgets import QApplication, QRadioButton, QHeaderView, QGroupBox, QDialog, QLineEdit, QLabel, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDate, QDir, QSettings
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Settings Dialog ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Settings(QDialog):
# +++++++++++++++++++++++++++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self,temp_config,parent = None):
        QDialog.__init__(self, parent)
        self.default_temp_config = temp_config
        self.temp_config = temp_config

        if self.temp_config['language'] == "georgian":
            Geo_Checked = True
            Eng_Checked = False
        else:
            Geo_Checked = False
            Eng_Checked = True
        
        self.setWindowTitle("პარამეტრები")
        self.setWindowIcon(QtGui.QIcon("icon/settings.png"))                         # Set main window icon

        self.groupBox_language = QGroupBox("ენა")                                    # create groupbox with lane
        self.groupBox_language.setAlignment(Qt.AlignCenter)

        self.groupBox_window_size = QGroupBox("ფანჯრის ზომა")                                    # create groupbox with lane
        self.groupBox_window_size.setAlignment(Qt.AlignCenter)
 
        VLbox = QVBoxLayout()
        VLbox.addWidget(self.groupBox_language)
        VLbox.addWidget(self.groupBox_window_size)

        hboxLayout_language = QHBoxLayout()
        hboxLayout_size = QHBoxLayout()

        self.Edit_length = QLineEdit()
        self.Edit_width = QLineEdit()

        self.Label_length = QLabel("სიგრძე")
        self.Label_width = QLabel("სიგანე")

        self.Edit_length.setText(str(self.temp_config['length']))
        self.Edit_width.setText(str(self.temp_config['width']))
        
        hboxLayout_size.addWidget(self.Label_length)
        hboxLayout_size.addWidget(self.Edit_length)
        hboxLayout_size.addWidget(self.Label_width)

        hboxLayout_size.addWidget(self.Edit_width)

        self.radioButton1 = QRadioButton("ქართული")                       # create radiobutton1
        self.radioButton1.setChecked(Geo_Checked)                                 # set radiobutton1 as default ticked
        self.radioButton1.setIcon(QtGui.QIcon("icon/georgia.png"))          # set icon on radiobutton1
        self.radioButton1.setIconSize(QtCore.QSize(40,40))                 # set icon size
        self.radioButton1.toggled.connect(self.geo)                        # create radiobutton1 and "OnRadioBtn" function conection
        hboxLayout_language.addWidget(self.radioButton1)                   # add radiobutton1 in horizontal layout

        self.radioButton2 = QRadioButton("ინგლისური")                     # create radiobutton2
        self.radioButton2.setChecked(Eng_Checked)
        self.radioButton2.setIcon(QtGui.QIcon("icon/english.png"))          # set icon on radiobutton2
        self.radioButton2.setIconSize(QtCore.QSize(40,40))                 # set icon size
        hboxLayout_language.addWidget(self.radioButton2)                   # add radiobutton2 in horizontal layout
        self.radioButton2.toggled.connect(self.eng)

        self.ApplySet = QPushButton("დადასტურება",self)
        self.CancelSet = QPushButton("გაუქმება",self)
        self.ApplySet.clicked.connect(self.applySettings)
        self.CancelSet.clicked.connect(self.CancelSettings)

        self.groupBox_language.setLayout(hboxLayout_language)              # in group box set horizontal layout
        self.groupBox_window_size.setLayout(hboxLayout_size)               # in group box set horizontal layout

        VLbox.addWidget(self.ApplySet)
        VLbox.addWidget(self.CancelSet)

        if self.temp_config['language'] == "georgian":
            self.geo()
        else:
            self.eng()

        self.setLayout(VLbox)
# ++++++++++++++++++++++++++++++++++++++++++++ Georgian language option ++++++++++++++++++++++++++++++++++++++++++++
    def geo(self):
        if self.radioButton1.isChecked():
            self.ApplySet.setText("დადასტურება")
            self.CancelSet.setText("გაუქმება")
            self.groupBox_language.setTitle("ენა")
            self.groupBox_window_size.setTitle("ფანჯრის ზომა")
            self.setWindowTitle("პარამეტრები")
            self.radioButton1.setText("ქართული")
            self.radioButton2.setText("ინგლისური")
            self.Label_length.setText("სიგრძე")
            self.Label_width.setText("სიგანე")
            self.temp_config['language'] = "georgian"
# +++++++++++++++++++++++++++++++++++++++++++++ English language option ++++++++++++++++++++++++++++++++++++++++++++
    def eng(self):
        if self.radioButton2.isChecked():
            self.ApplySet.setText("Apply")
            self.CancelSet.setText("Cancel")
            self.groupBox_language.setTitle("Language")
            self.groupBox_window_size.setTitle("Window Size")
            self.setWindowTitle("Settings")
            self.radioButton1.setText("Georgian")
            self.radioButton2.setText("English")
            self.Label_length.setText("Length")
            self.Label_width.setText("width")
            self.temp_config['language'] = "english"
# +++++++++++++++++++++++++++++++++++++++++++++++++ Apply Settings +++++++++++++++++++++++++++++++++++++++++++++++++
    def applySettings(self):
        try:
            self.temp_config['length'] = int(self.Edit_length.text())
            self.temp_config['width'] = int(self.Edit_width.text())
        except ValueError:
            pass
        self.close()
# +++++++++++++++++++++++++++++++++++++++++++++++++ Cancel Settings ++++++++++++++++++++++++++++++++++++++++++++++++
    def CancelSettings(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    temp_config = {'tableColNumber' : 6,'language' : 'georgian','length': 1850, 'width' : 900}
    diag = Settings(temp_config)
    diag.exec_()
    sys.exit(app.exec_())