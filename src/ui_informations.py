# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'informations.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QWidget)

class Ui_DialogInformation(object):
    def setupUi(self, DialogInformation):
        if not DialogInformation.objectName():
            DialogInformation.setObjectName(u"DialogInformation")
        DialogInformation.resize(400, 300)
        self.buttonBox = QDialogButtonBox(DialogInformation)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(DialogInformation)
        self.buttonBox.accepted.connect(DialogInformation.accept)
        self.buttonBox.rejected.connect(DialogInformation.reject)

        QMetaObject.connectSlotsByName(DialogInformation)
    # setupUi

    def retranslateUi(self, DialogInformation):
        DialogInformation.setWindowTitle(QCoreApplication.translate("DialogInformation", u"Dialog", None))
    # retranslateUi

