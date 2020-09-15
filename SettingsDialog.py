from PyQt5.QtWidgets import (QApplication, QRadioButton, QGroupBox,
                             QDialog, QLineEdit, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import sys
# ~~~~~~~~~~~~~~~~~~~~~~~~~ Settings Dialog ~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Settings(QDialog):
# ++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++
    def __init__(self, config, parent = None):
        QDialog.__init__(self, parent)
        self.applayState = False
        self.config = config
        self.language = config['language']

        if self.language == "georgian":
            Geo_Checked = True
            Eng_Checked = False
        else:
            Geo_Checked = False
            Eng_Checked = True
        
        self.setWindowTitle("პარამეტრები")
        self.setWindowIcon(QtGui.QIcon("icon/setting.svg"))

        self.groupBox_language = QGroupBox("ენა")
        self.groupBox_language.setAlignment(Qt.AlignCenter)

        self.groupBox_window_size = QGroupBox("ფანჯრის ზომა")
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

        self.Edit_length.setText(str(self.config['length']))
        self.Edit_width.setText(str(self.config['width']))
        
        hboxLayout_size.addWidget(self.Label_length)
        hboxLayout_size.addWidget(self.Edit_length)
        hboxLayout_size.addWidget(self.Label_width)
        hboxLayout_size.addWidget(self.Edit_width)

        self.Geo_radioButton = QRadioButton("ქართული")
        self.Geo_radioButton.setChecked(Geo_Checked)
        self.Geo_radioButton.setIcon(QtGui.QIcon("icon/georgia.png"))
        self.Geo_radioButton.setIconSize(QtCore.QSize(40,40))
        self.Geo_radioButton.toggled.connect(self.geo)
        hboxLayout_language.addWidget(self.Geo_radioButton)

        self.Eng_radioButton = QRadioButton("ინგლისური")
        self.Eng_radioButton.setChecked(Eng_Checked)
        self.Eng_radioButton.setIcon(QtGui.QIcon("icon/english.png"))
        self.Eng_radioButton.setIconSize(QtCore.QSize(40,40))
        hboxLayout_language.addWidget(self.Eng_radioButton)
        self.Eng_radioButton.toggled.connect(self.eng)

        self.ApplySet = QPushButton("დადასტურება",self)
        self.CancelSet = QPushButton("გაუქმება",self)
        self.ApplySet.clicked.connect(self.applySettings)
        self.CancelSet.clicked.connect(self.CancelSettings)

        self.groupBox_language.setLayout(hboxLayout_language)
        self.groupBox_window_size.setLayout(hboxLayout_size)

        VLbox.addWidget(self.ApplySet)
        VLbox.addWidget(self.CancelSet)

        if self.language == "georgian":
            self.geo()
        else:
            self.eng()

        self.setLayout(VLbox)
# ++++++++++++++++++++ Georgian language option +++++++++++++++++++++++
    def geo(self):
        if self.Geo_radioButton.isChecked():
            self.ApplySet.setText("დადასტურება")
            self.CancelSet.setText("გაუქმება")
            self.groupBox_language.setTitle("ენა")
            self.groupBox_window_size.setTitle("ფანჯრის ზომა")
            self.setWindowTitle("პარამეტრები")
            self.Geo_radioButton.setText("ქართული")
            self.Eng_radioButton.setText("ინგლისური")
            self.Label_length.setText("სიგრძე")
            self.Label_width.setText("სიგანე")
            self.language = "georgian"
# +++++++++++++++++++++ English language option +++++++++++++++++++++++
    def eng(self):
        if self.Eng_radioButton.isChecked():
            self.ApplySet.setText("Apply")
            self.CancelSet.setText("Cancel")
            self.groupBox_language.setTitle("Language")
            self.groupBox_window_size.setTitle("Window Size")
            self.setWindowTitle("Settings")
            self.Geo_radioButton.setText("Georgian")
            self.Eng_radioButton.setText("English")
            self.Label_length.setText("Length")
            self.Label_width.setText("width")
            self.language = "english"
# +++++++++++++++++++++++++++ get Settings ++++++++++++++++++++++++++++
    def getSettings(self):
        return self.config, self.applayState
# +++++++++++++++++++++++++ Apply Settings ++++++++++++++++++++++++++++
    def applySettings(self):
        try:
            self.config['length'] = int(self.Edit_length.text())
            self.config['width'] = int(self.Edit_width.text())
            self.config['language'] = self.language
        except ValueError:
            pass
        self.applayState = True
        self.close()
# +++++++++++++++++++++++++ Cancel Settings +++++++++++++++++++++++++++
    def CancelSettings(self):
        self.applayState = False
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = {'language' : 'georgian','length': 1850, 'width' : 900}
    Settingsdialog = Settings(config)
    Settingsdialog.exec_()
    settings, acceptState = Settingsdialog.getSettings()
    print(settings)
    print(acceptState)