import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

class HelpWindow(object):
    def __init__(self, html_content):
        self.html_content = html_content

    def setup_ui(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(400, 420)

        # Устанавливаем layout, подходящий для QDialog
        layout = QtWidgets.QVBoxLayout(HelpWindow)

        self.label = QtWidgets.QLabel(parent=HelpWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")

        layout.addWidget(self.label)  # Добавляем виджет в layout

        self.retranslate_ui(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslate_ui(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "Справка"))
        self.label.setText(_translate("HelpWindow", self.html_content))

def load_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

class MainWindow():
    def setup_ui(self, QMainWindow : QtWidgets.QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.setEnabled(True)
        QMainWindow.resize(720, 488)

        self.central_widget = QtWidgets.QWidget(parent=QMainWindow)
        self.central_widget.setMinimumSize(QtCore.QSize(0, 470))
        self.central_widget.setObjectName("central_widget")

        self.btn_select_file = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_select_file.setGeometry(QtCore.QRect(4, 4, 216, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_select_file.setFont(font)
        self.btn_select_file.setObjectName("btn_select_file")
        self.btn_select_file.clicked.connect(self.select_file)

        self.btn_toggle_view = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_toggle_view.setGeometry(QtCore.QRect(224, 4, 216, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_toggle_view.setFont(font)
        self.btn_toggle_view.setObjectName("btn_toggle_view")

        self.btn_open_help = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_open_help.setGeometry(QtCore.QRect(588, 4, 128, 48))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_open_help.setFont(font)
        self.btn_open_help.setObjectName("btn_open_help")
        self.btn_open_help.clicked.connect(self.open_help)

        self.label_before_select = QtWidgets.QLabel(parent=self.central_widget)
        self.label_before_select.setGeometry(QtCore.QRect(220, 120, 280, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_before_select.setFont(font)
        self.label_before_select.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_before_select.setObjectName("label_before_select")

        self.convert = QtWidgets.QPushButton(parent=self.central_widget)
        self.convert.setGeometry(QtCore.QRect(240, 240, 240, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.convert.setFont(font)
        self.convert.setDefault(False)
        self.convert.setObjectName("convert")

        QMainWindow.setCentralWidget(self.central_widget)

        self.retranslate_ui(QMainWindow)

        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

    def retranslate_ui(self, QMainWindow : QtWidgets.QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "QMainWindow"))
        self.btn_select_file.setText(_translate("QMainWindow", "Выбрать файл"))
        self.btn_toggle_view.setText(_translate("QMainWindow", "Версия для слабовидящих"))
        self.btn_open_help.setText(_translate("QMainWindow", "Справка"))
        self.label_before_select.setText(_translate("QMainWindow", "Выберите файл для конвертации"))
        self.convert.setText(_translate("QMainWindow", "Конвертировать"))

    def open_help(self):
        logging.debug('ui.MainWindow.open_help() entered')
        self.dialog = QtWidgets.QDialog()
        html_file_path = os.path.join(os.path.dirname(__file__), 'help_content.html')
        html_content = load_html_content(html_file_path)
        self.ui_help = HelpWindow(html_content)
        self.ui_help.setup_ui(self.dialog)
        self.dialog.exec()

    def select_file(self):
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
    qmw = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(qmw)
    qmw.show()
    sys.exit(app.exec())
