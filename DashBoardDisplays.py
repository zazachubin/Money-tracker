# ---------------------------------------------------- Libraries ---------------------------------------------------
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPalette, QPixmap, QColor
from PyQt5.QtCore import Qt
import sys

class DashBoardDisplay(QWidget):
# ++++++++++++++++++++++++++++ __init__ +++++++++++++++++++++++++++++++
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setStyleSheet("""QLCDNumber {  margin: 1px;
                                            padding: 7px;
                                            background-color: rgba(100,255,255,20);
                                            color: rgb(255,255,255);
                                            border-style: solid;
                                            border-radius: 8px;
                                            border-width: 3px;
                                            border-color: rgba(0,140,255,255);}""")
############################## Layouts ################################
        Vlayout = QVBoxLayout()
        SubHlayout_1 = QHBoxLayout()
        SubHlayout_2 = QHBoxLayout()
        SubHlayout_3 = QHBoxLayout()
        SubHlayout_4 = QHBoxLayout()
        SubHlayout_5 = QHBoxLayout()
        SubHlayout_6 = QHBoxLayout()
############################### Ruble #################################
        self.dysplay_Ruble = QLCDNumber()
        self.dysplay_Ruble.setDigitCount(11)
        Icon_Ruble = QLabel()
        Icon_Ruble.setPixmap(QPixmap("icon/Ruble.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_1.addWidget(Icon_Ruble,10)
        SubHlayout_1.addWidget(self.dysplay_Ruble,90)
############################### Dollar ################################
        self.dysplay_Dollar = QLCDNumber()
        self.dysplay_Dollar.setDigitCount(11)
        Icon_Dollar = QLabel()
        Icon_Dollar.setPixmap(QPixmap("icon/Dollar.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_2.addWidget(Icon_Dollar,10)
        SubHlayout_2.addWidget(self.dysplay_Dollar,90)
################################ Euro #################################
        self.dysplay_Euro = QLCDNumber()
        self.dysplay_Euro.setDigitCount(11)
        Icon_Euro = QLabel()
        Icon_Euro.setPixmap(QPixmap("icon/Euro.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_3.addWidget(Icon_Euro,10)
        SubHlayout_3.addWidget(self.dysplay_Euro,90)
############################### Franc #################################
        self.dysplay_Franc = QLCDNumber()
        self.dysplay_Franc.setDigitCount(11)
        Icon_Franc = QLabel()
        Icon_Franc.setPixmap(QPixmap("icon/swiss-franc.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_4.addWidget(Icon_Franc,10)
        SubHlayout_4.addWidget(self.dysplay_Franc,90)
################################ Lari #################################
        self.dysplay_Lari = QLCDNumber()
        self.dysplay_Lari.setDigitCount(11)
        Icon_Lari = QLabel()
        Icon_Lari.setPixmap(QPixmap("icon/Lari.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_5.addWidget(Icon_Lari,10)
        SubHlayout_5.addWidget(self.dysplay_Lari,90)
################################ Yuan #################################
        self.dysplay_Yuan = QLCDNumber()
        self.dysplay_Yuan.setDigitCount(11)
        Icon_Yuan = QLabel()
        Icon_Yuan.setPixmap(QPixmap("icon/yuan.svg").scaled(50, 50, Qt.KeepAspectRatio))

        SubHlayout_6.addWidget(Icon_Yuan,10)
        SubHlayout_6.addWidget(self.dysplay_Yuan,90)
########################### Setup Layouts #############################
        Vlayout.addLayout(SubHlayout_1)
        Vlayout.addLayout(SubHlayout_2)
        Vlayout.addLayout(SubHlayout_3)
        Vlayout.addLayout(SubHlayout_4)
        Vlayout.addLayout(SubHlayout_5)
        Vlayout.addLayout(SubHlayout_6)

        self.setLayout(Vlayout)
# +++++++++++++++++++++++++ Update display ++++++++++++++++++++++++++++
    def updateDisplay(self, data):
        self.dysplay_Ruble.display("%.2f" % (data[0]))
        self.dysplay_Dollar.display("%.2f" % (data[1]))
        self.dysplay_Euro.display("%.2f" % (data[2]))
        self.dysplay_Franc.display("%.2f" % (data[3]))
        self.dysplay_Lari.display("%.2f" % (data[4]))
        self.dysplay_Yuan.display("%.2f" % (data[5]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DashBoardDisplay()
    ex.updateDisplay([100,100.5,15.65,205.32,25.6,35.7])
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