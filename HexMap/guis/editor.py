# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_gui.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class PicButton(QtGui.QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix=self.pixmap_pressed

        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()
    def leaveEvent(Self, event):
        self.update()

    def sizeHint(self):
        return(QtCore.QSize(200,40))



class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1168, 695)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Forest = QtGui.QPushButton(self.centralwidget)
        self.Forest.setObjectName(_fromUtf8("Forest"))
        self.horizontalLayout.addWidget(self.Forest)
        self.Grassland = QtGui.QPushButton(self.centralwidget)
        self.Grassland.setObjectName(_fromUtf8("Grassland"))
        self.horizontalLayout.addWidget(self.Grassland)
        self.Ocean = QtGui.QPushButton(self.centralwidget)
        self.Ocean.setObjectName(_fromUtf8("Ocean"))
        self.horizontalLayout.addWidget(self.Ocean)
        self.pushButton_8 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.horizontalLayout.addWidget(self.pushButton_8)
        self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.horizontalLayout.addWidget(self.pushButton_7)
        self.pushButton_9 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.horizontalLayout.addWidget(self.pushButton_9)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_2.addWidget(self.graphicsView, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.brush = QtGui.QRadioButton(self.centralwidget)
        self.brush.setObjectName(_fromUtf8("brush"))
        self.verticalLayout_2.addWidget(self.brush)
        self.hand = QtGui.QRadioButton(self.centralwidget)
        self.hand.setObjectName(_fromUtf8("hand"))
        self.verticalLayout_2.addWidget(self.hand)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        
        self.brushTottle = QtGui.QPushButton(self.centralwidget)
        self.brushTottle.setObjectName(_fromUtf8("brushTottle"))
        self.verticalLayout_2.addWidget(self.brushTottle)
        self.write_erase = QtGui.QPushButton(self.centralwidget)
        self.write_erase.setObjectName(_fromUtf8("write_erase"))
        self.verticalLayout_2.addWidget(self.write_erase)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.biodiversity = QtGui.QSlider(self.centralwidget)
        self.biodiversity.setOrientation(QtCore.Qt.Vertical)
        self.biodiversity.setObjectName(_fromUtf8("biodiversity"))
        self.horizontalLayout_2.addWidget(self.biodiversity)
        self.temperature = QtGui.QSlider(self.centralwidget)
        self.temperature.setOrientation(QtCore.Qt.Vertical)
        self.temperature.setObjectName(_fromUtf8("temperature"))
        self.horizontalLayout_2.addWidget(self.temperature)
        self.rainfall = QtGui.QSlider(self.centralwidget)
        self.rainfall.setOrientation(QtCore.Qt.Vertical)
        self.rainfall.setObjectName(_fromUtf8("rainfall"))
        self.horizontalLayout_2.addWidget(self.rainfall)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.verticalLayout_2.addWidget(self.pushButton_6)

        # -------------------- quit
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        #self.pushButton_5.clicked.connect( QtCore.QCoreApplication.instance().quit)

        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        # ------------------------- lcd! 
        self.idBar = QtGui.QLCDNumber(self.centralwidget)
        self.idBar.setObjectName(_fromUtf8("idBar"))
        self.gridLayout_2.addWidget(self.idBar, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1168, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Forest.setText(_translate("MainWindow", "Forest", None))
        self.Grassland.setText(_translate("MainWindow", "Grassland", None))
        self.Ocean.setText(_translate("MainWindow", "Ocean", None))
        self.pushButton_8.setText(_translate("MainWindow", "Arctic", None))
        self.pushButton_7.setText(_translate("MainWindow", "Desert", None))
        self.pushButton_9.setText(_translate("MainWindow", "Mountains", None))
        self.brush.setText(_translate("MainWindow", "Brush", None))
        self.hand.setText(_translate("MainWindow", "Hand", None))
        self.brushTottle.setText(_translate("MainWindow", "Toggle Brush", None))
        self.write_erase.setText(_translate("MainWindow", "Write/Erase", None))
        self.label.setText(_translate("MainWindow", "Bio  Temp  Rain", None))
        self.pushButton_4.setText(_translate("MainWindow", "Save", None))
        self.pushButton_6.setText(_translate("MainWindow", "Save as...", None))
        self.pushButton_5.setText(_translate("MainWindow", "Back", None))
        self.label_2.setText(_translate("MainWindow", "Unnamed", None))

