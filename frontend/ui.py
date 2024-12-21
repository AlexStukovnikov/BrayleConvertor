import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import logging
from backend.convert import convert

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=1)

class HelpWindow():
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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as e:
        # Обработка ошибки чтения файла
        logging.error(f"Ошибка чтения файла: {e}")
        return ""

class MainWindow():
    def __init__(self):
        self.is_grayscale = False

    def setup_ui(self, QMainWindow : QtWidgets.QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.setEnabled(True)
        QMainWindow.resize(720, 488)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(255, 250, 250))
        QMainWindow.setPalette(palette)

        self.central_widget = QtWidgets.QWidget(parent=QMainWindow)
        self.central_widget.setMinimumSize(QtCore.QSize(0, 470))
        self.central_widget.setObjectName("central_widget")

        self.shortcuts = {
            "select_file" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"),self.central_widget),
            "convert_file" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+K"),self.central_widget),
            "open_help" : QtGui.QShortcut(QtGui.QKeySequence("F1"),self.central_widget),
            "toggle_view" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+V"),self.central_widget),
        }

        self.btn_select_file = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_select_file.setGeometry(QtCore.QRect(4, 4, 216, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_select_file.setFont(font)
        self.btn_select_file.setObjectName("btn_select_file")
        self.btn_select_file.clicked.connect(self.select_file)
        self.shortcuts["select_file"].activated.connect(self.select_file)

        self.btn_toggle_view = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_toggle_view.setGeometry(QtCore.QRect(224, 4, 216, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_toggle_view.setFont(font)
        self.btn_toggle_view.setObjectName("btn_toggle_view")
        self.btn_toggle_view.clicked.connect(self.toggle_view)
        self.shortcuts["toggle_view"].activated.connect(self.toggle_view)

        self.btn_open_help = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_open_help.setGeometry(QtCore.QRect(588, 4, 128, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_open_help.setFont(font)
        self.btn_open_help.setObjectName("btn_open_help")
        self.btn_open_help.clicked.connect(self.open_help)
        self.shortcuts["open_help"].activated.connect(self.open_help)

        self.label_before_select = QtWidgets.QLabel(parent=self.central_widget)
        self.label_before_select.setGeometry(QtCore.QRect(220, 120, 280, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_before_select.setFont(font)
        self.label_before_select.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_before_select.setObjectName("label_before_select")

        self.btn_convert_file = QtWidgets.QPushButton(parent=self.central_widget)
        self.btn_convert_file.setGeometry(QtCore.QRect(240, 240, 240, 80))
        self.btn_convert_file.setStyleSheet("background-color: #FFC0CB")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_convert_file.setFont(font)
        self.btn_convert_file.setDefault(False)
        self.btn_convert_file.setObjectName("btn_convert_file")
        self.btn_convert_file.clicked.connect(self.convert_file)
        self.shortcuts["convert_file"].activated.connect(self.convert_file)

        QMainWindow.setCentralWidget(self.central_widget)

        self.retranslate_ui(QMainWindow)

        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

        #! TEMPORARY
        self.output_file_path = os.path.join(os.path.dirname(__file__), "output.brf")

    def retranslate_ui(self, QMainWindow : QtWidgets.QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "QMainWindow"))
        self.btn_select_file.setText(_translate("QMainWindow", "Выбрать файл"))
        self.btn_toggle_view.setText(_translate("QMainWindow", "Версия для слабовидящих"))
        self.btn_open_help.setText(_translate("QMainWindow", "Справка"))
        self.label_before_select.setText(_translate("QMainWindow", "Выберите файл для конвертации"))
        self.btn_convert_file.setText(_translate("QMainWindow", "Конвертировать"))

    def open_help(self):
        logging.debug('ui.MainWindow.open_help() entered')
        self.dialog = QtWidgets.QDialog()
        html_file_path = os.path.join(os.path.dirname(__file__), 'help_content.html')
        html_content = load_html_content(html_file_path)
        if html_content == "":
            # Обработка ошибки чтения файла справки
            logging.error("Не удалось загрузить файл справки")
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Не удалось загрузить файл справки")
            msg.exec()
            return
        self.ui_help = HelpWindow(html_content)
        self.ui_help.setup_ui(self.dialog)
        self.dialog.exec()

    def select_file(self):
        # Открытие диалога выбора файла
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Выберите файл", "", "Все файлы (*)"
        )

        # Обработка ошибки чтения файла
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    pass  # Код, который использует содержимое файла
            except FileNotFoundError as e:
                # Обработка ошибки чтения файла
                logging.error(f"Ошибка чтения файла: {e}")
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Не удалось прочитать выбранный файл")
                msg.exec()
                return
        # Вывод названия файла
        if file_path:
            self.target_file_path = file_path
            self.label_before_select.setText(f"Выбранный файл: {file_path}")

    def convert_file(self):
        if not self.target_file_path:
            logging.debug("ui.MainWindow.convert_file did not find target_file_path")
            return
        convert(self.target_file_path, self.output_file_path)
        self.popup = QtWidgets.QMessageBox()
        self.popup.setText(f"File {self.target_file_path} converted successfully and saved at {self.output_file_path}")

    def toggle_view(self):
        logging.debug('ui.MainWindow.toggle_view() entered')
        if self.is_grayscale:
            self.is_grayscale = False
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(255, 250, 250))
            qmw.setPalette(palette)

            self.btn_convert_file.setStyleSheet("background-color: #FFC0CB")
            self.btn_toggle_view.setText("Версия для слабовидящих")

            logging.info('Changed into colored mode')
        else:
            self.is_grayscale = True
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(235, 235, 235))
            qmw.setPalette(palette)

            self.btn_convert_file.setStyleSheet("background-color: #C0C0C0")
            self.btn_toggle_view.setText("Цветная версия")

            logging.info('Changed into bw mode')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qmw = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(qmw)
    qmw.show()
    sys.exit(app.exec())
