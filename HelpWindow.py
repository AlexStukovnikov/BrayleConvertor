# Form implementation generated from reading ui file 'HelpWindow.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(400, 420)

        self.centralwidget = QtWidgets.QWidget(parent=HelpWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 420))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")

        HelpWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "Справка"))

        self.label.setText(_translate("HelpWindow", "<html>"
                                                    "<head/>"
                                                    "<body>"
                                                    "<p align=\"justify\">"
                                                    "<span style=\" font-size:12pt;\">"
                                                    "Тут надо написать описание приложения"
                                                    "<br/>"
                                                    "<br/>"
                                                    "Клавиатурные сочетания:"
                                                    "</span></p>"
                                                    "<p align=\"justify\"><span style=\" font-size:12pt;\"> - Ctrl + O: открыть файл для конвертации</span></p>"
                                                    "<p align=\"justify\"><span style=\" font-size:12pt;\"> - Esc: отменить выбор файла</span></p>"
                                                    "<p align=\"justify\"><span style=\" font-size:12pt;\"> - Ctrl + K: конвертировать файл</span></p>"
                                                    "<p align=\"justify\"><span style=\" font-size:12pt;\"> - Ctrl + S: сохранить преобразованный файл</span></p>"
                                                    "<p align=\"justify\"><span style=\" font-size:12pt;\"> - Ctrl + V: смена режима (слабозрячий/зрячий)</span></p>"
                                                    "</body>"
                                                    "</html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HelpWindow = QtWidgets.QMainWindow()
    ui = Ui_HelpWindow()
    ui.setupUi(HelpWindow)
    HelpWindow.show()
    sys.exit(app.exec())