import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from HelpWindow import Ui_HelpWindow

class Ui_BrayleConvertor(object):
    def setupUi(self, BrayleConvertor):
        BrayleConvertor.setObjectName("BrayleConvertor")
        BrayleConvertor.setEnabled(True)
        BrayleConvertor.resize(720, 488)

        self.centralwidget = QtWidgets.QWidget(parent=BrayleConvertor)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 470))
        self.centralwidget.setObjectName("centralwidget")

        self.select_file = QtWidgets.QPushButton(parent=self.centralwidget)
        self.select_file.setGeometry(QtCore.QRect(4, 4, 216, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.select_file.setFont(font)
        self.select_file.setObjectName("select_file")
        self.select_file.clicked.connect(self.select_file_action) 

        self.bw_version_change = QtWidgets.QPushButton(parent=self.centralwidget)
        self.bw_version_change.setGeometry(QtCore.QRect(224, 4, 216, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bw_version_change.setFont(font)
        self.bw_version_change.setObjectName("bw_version_change")

        self.help_opener = QtWidgets.QPushButton(parent=self.centralwidget)
        self.help_opener.setGeometry(QtCore.QRect(588, 4, 128, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.help_opener.setFont(font)
        self.help_opener.setObjectName("help_opener")
        self.help_opener.clicked.connect(self.open_help)

        self.label_before_select = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_before_select.setGeometry(QtCore.QRect(220, 120, 280, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_before_select.setFont(font)
        self.label_before_select.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_before_select.setObjectName("label_before_select")

        self.convert = QtWidgets.QPushButton(parent=self.centralwidget)
        self.convert.setGeometry(QtCore.QRect(240, 240, 240, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.convert.setFont(font)
        self.convert.setDefault(False)
        self.convert.setObjectName("convert")

        BrayleConvertor.setCentralWidget(self.centralwidget)

        self.retranslateUi(BrayleConvertor)

        QtCore.QMetaObject.connectSlotsByName(BrayleConvertor)

    def retranslateUi(self, BrayleConvertor):
        _translate = QtCore.QCoreApplication.translate
        BrayleConvertor.setWindowTitle(_translate("BrayleConvertor", "BrayleConvertor"))
        self.select_file.setText(_translate("BrayleConvertor", "Выбрать файл"))
        self.bw_version_change.setText(_translate("BrayleConvertor", "Версия для слабовидящих"))
        self.help_opener.setText(_translate("BrayleConvertor", "Справка"))
        self.label_before_select.setText(_translate("BrayleConvertor", "Выберите файл для конвертации"))
        self.convert.setText(_translate("BrayleConvertor", "Конвертировать"))

    def open_help(self):
        print("проверка поступления сигнала")
        self.dialog = QtWidgets.QDialog() 
        self.ui_help = Ui_HelpWindow()
        self.ui_help.setupUi(self.dialog)
        self.dialog.exec() 

    def select_file_action(self):
        # Открытие диалога выбора файла
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Выберите файл", "", "Все файлы (*)"
        )
        # Вывод названия файла
        if file_path:  
            file_name = file_path.split("/")[-1] 
            self.label_before_select.setText(file_name)  


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    BrayleConvertor = QtWidgets.QMainWindow()
    ui = Ui_BrayleConvertor()
    ui.setupUi(BrayleConvertor)
    BrayleConvertor.show()
    sys.exit(app.exec())
