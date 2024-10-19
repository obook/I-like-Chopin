# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLayout, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(538, 336)
        self.gridLayout_2 = QGridLayout(MainWindow)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.plainTextEdit = QPlainTextEdit(MainWindow)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setAcceptDrops(True)

        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)

        self.pushButton_Load = QPushButton(MainWindow)
        self.pushButton_Load.setObjectName(u"pushButton_Load")

        self.gridLayout.addWidget(self.pushButton_Load, 1, 0, 1, 1)

        self.pushButton_Quit = QPushButton(MainWindow)
        self.pushButton_Quit.setObjectName(u"pushButton_Quit")

        self.gridLayout.addWidget(self.pushButton_Quit, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_Load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.pushButton_Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
    # retranslateUi

