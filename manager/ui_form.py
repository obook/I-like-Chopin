# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(443, 281)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_Abort = QPushButton(self.centralwidget)
        self.pushButton_Abort.setObjectName(u"pushButton_Abort")

        self.horizontalLayout.addWidget(self.pushButton_Abort)

        self.pushButton_Remove_Item = QPushButton(self.centralwidget)
        self.pushButton_Remove_Item.setObjectName(u"pushButton_Remove_Item")

        self.horizontalLayout.addWidget(self.pushButton_Remove_Item)

        self.pushButton_Save = QPushButton(self.centralwidget)
        self.pushButton_Save.setObjectName(u"pushButton_Save")

        self.horizontalLayout.addWidget(self.pushButton_Save)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 443, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Playlist Manager", None))
        self.pushButton_Abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.pushButton_Remove_Item.setText(QCoreApplication.translate("MainWindow", u"Remove Item", None))
        self.pushButton_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi
