# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'informations.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QPushButton,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_DialogInformation(object):
    def setupUi(self, DialogInformation):
        if not DialogInformation.objectName():
            DialogInformation.setObjectName(u"DialogInformation")
        DialogInformation.resize(479, 350)
        self.pushButton_Close = QPushButton(DialogInformation)
        self.pushButton_Close.setObjectName(u"pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(200, 310, 81, 25))
        self.textBrowser = QTextBrowser(DialogInformation)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 301, 281))
        self.textBrowser.setOpenExternalLinks(True)
        self.formLayoutWidget = QWidget(DialogInformation)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(320, 10, 141, 281))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(DialogInformation)

        QMetaObject.connectSlotsByName(DialogInformation)
    # setupUi

    def retranslateUi(self, DialogInformation):
        DialogInformation.setWindowTitle(QCoreApplication.translate("DialogInformation", u"Dialog", None))
        self.pushButton_Close.setText(QCoreApplication.translate("DialogInformation", u"Close", None))
    # retranslateUi
