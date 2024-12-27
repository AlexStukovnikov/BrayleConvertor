import os
from PyQt6 import QtCore, QtGui, QtWidgets
import logging
from backend.convert import convert
from typing import Callable
from functools import wraps
from music21.converter import ConverterException, ConverterFileException
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=1)

def _create_popup(parent=None, title=None, desc=None):
    popup = QtWidgets.QMessageBox(parent=parent)
    popup.setWindowTitle(title)
    popup.setText(desc)
    popup.exec()

def _error_handler(*exceptions: Exception, title=None, desc=None, level=None):
    def _handler(f: Callable):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except exceptions as e:
                nonlocal title
                nonlocal desc
                if not title: title = e.__notes__[0]
                if not desc: desc = e.__notes__[1]
                _create_popup(title=title,desc=desc)
                logging.warning(e) if not level else logging.log(int(e.__notes__[2]),e)
        return _wrapper
    return _handler

_oserror_handler = _error_handler(OSError, title="Ошибка выбора файла", desc="Файл не найден: проверьте разрешения выбранного файла или родительской папки")

class HelpWindow(QtWidgets.QDialog):
    def __init__(self, html_content, parent=None):
        super().__init__(parent=parent)
        self.html_content = html_content
        self._error_handler = _error_handler
        self.setWindowTitle("Справка")

        self.resize(400, 420)
        self.setObjectName("HelpWindow")

        self.label = QtWidgets.QLabel(self.html_content, parent=self)
        self.label.setFont(QtGui.QFont(None,12))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

#        self.retranslate_ui()

#    def retranslate_ui(self):
#        _translate = QtCore.QCoreApplication.translate
#        self.setWindowTitle(_translate("HelpWindow", "Справка"))
#        self.label.setText(_translate("HelpWindow", self.html_content))



class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")

    def setup_ui(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(200, 200)

        layout = QtWidgets.QVBoxLayout(self)

        self.radio_option_1 = QtWidgets.QRadioButton("После конвертации автоматически сохранять по пути", self)
        self.radio_option_2 = QtWidgets.QRadioButton("После конвертации спрашивать место сохранения", self)

        layout.addWidget(self.radio_option_1)
        layout.addWidget(self.radio_option_2)

        self.radio_option_1.setChecked(True)

class MainWindow(QtWidgets.QMainWindow):
    global _oserror_handler
    global _error_handler

    @_oserror_handler
    def __init__(self):
        super().__init__()

        html_file_path = os.path.join(os.path.dirname(__file__), 'help_content.html')
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        

        self.help_window = HelpWindow(html_content)

        self.is_grayscale = False

        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(720, 488)
        self.setWindowTitle("Braillehoven")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(255, 250, 250))
        self.setPalette(palette)

        self.shortcuts = {
            "select_file" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"),self),
            "convert_file" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+K"),self),
            "open_help" : QtGui.QShortcut(QtGui.QKeySequence("F1"),self),
            "toggle_view" : QtGui.QShortcut(QtGui.QKeySequence("Ctrl+V"),self),
        }
        
        self.btn_select_file = QtWidgets.QPushButton("Выбрать файл", self)
        self.btn_select_file.setGeometry(QtCore.QRect(4, 4, 216, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_select_file.setFont(font)
        self.btn_select_file.setObjectName("btn_select_file")
        self.btn_select_file.clicked.connect(self.select_file)
        self.shortcuts["select_file"].activated.connect(self.select_file)

        self.btn_toggle_view = QtWidgets.QPushButton("Версия для слабовидящих", parent=self)
        self.btn_toggle_view.setGeometry(QtCore.QRect(224, 4, 216, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_toggle_view.setFont(font)
        self.btn_toggle_view.setObjectName("btn_toggle_view")
        self.btn_toggle_view.clicked.connect(self.toggle_view)
        self.shortcuts["toggle_view"].activated.connect(self.toggle_view)

        self.btn_open_help = QtWidgets.QPushButton("Справка", self)
        self.btn_open_help.setGeometry(QtCore.QRect(536, 4, 128, 48))
        self.btn_select_file.setStyleSheet("background-color: white")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_open_help.setFont(font)
        self.btn_open_help.setObjectName("btn_open_help")
        self.btn_open_help.clicked.connect(self.open_help)
        self.shortcuts["open_help"].activated.connect(self.open_help)

        self.btn_settings = QtWidgets.QPushButton("S", parent=self)
        self.btn_settings.setGeometry(QtCore.QRect(668, 4, 48, 48))
        self.btn_settings.setStyleSheet("background-color: white")
        self.btn_settings.setFont(font)
        self.btn_settings.clicked.connect(self.open_settings_menu)
        self.label_before_select = QtWidgets.QLabel(self)
        self.label_before_select.setGeometry(QtCore.QRect(220, 120, 280, 40))
        font = QtGui.QFont()
        font.setPointSize(12)

        self.label_before_select = QtWidgets.QLabel("Выберите файл для конвертации", parent=self)
        self.label_before_select.setGeometry(QtCore.QRect(220, 120, 280, 40))
        self.label_before_select.setWordWrap(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_before_select.setFont(font)
        self.label_before_select.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_before_select.setObjectName("label_before_select")

        self.btn_convert_file = QtWidgets.QPushButton("Конвертировать", self)
        self.btn_convert_file.setGeometry(QtCore.QRect(240, 240, 240, 80))
        self.btn_convert_file.setStyleSheet("background-color: #FFC0CB")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_convert_file.setFont(font)
        self.btn_convert_file.setDefault(False)
        self.btn_convert_file.setObjectName("btn_convert_file")
        self.btn_convert_file.clicked.connect(self.convert_file)
        self.shortcuts["convert_file"].activated.connect(self.convert_file)

        self.save_button = QtWidgets.QPushButton("Сохранить", parent=self)
        self.save_button.setGeometry(QtCore.QRect(240, 340, 240, 40))
        self.save_button.setStyleSheet("background-color: #87CEFA")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.save_button.setFont(font)
        self.save_button.hide()
        self.save_button.clicked.connect(self.save_manually)

        # self.retranslate_ui()

        #! TEMPORARY
        self.output_file_path = os.path.join(os.path.dirname(__file__), "output.brf")

#    def retranslate_ui(self):
#        _translate = QtCore.QCoreApplication.translate
#        self.setWindowTitle(_translate("QMainWindow", "QMainWindow"))
#        self.btn_select_file.setText(_translate("QMainWindow", "Выбрать файл"))
#        self.btn_toggle_view.setText(_translate("QMainWindow", "Версия для слабовидящих"))
#        self.btn_open_help.setText(_translate("QMainWindow", "Справка"))
#        self.label_before_select.setText(_translate("QMainWindow", "Выберите файл для конвертации"))
#        self.btn_convert_file.setText(_translate("QMainWindow", "Конвертировать"))

    '''
    Apparently, QT signals pass implicit argument(s?) to a slot function: in this case, button's status (such as <bool> clicked), and normally this wouldn't matter, but if we use decorator on a function, it all falls apart, so we must put _event (or *args) as last argument in every single slot function
    '''
    def open_help(self, _event=None):
        logging.debug('ui.MainWindow.open_help() entered')

        if self.help_window.isVisible():
            self.help_window.hide()
        else:
            self.help_window.show()

    @_oserror_handler
    def select_file(self, _event=None):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Выберите файл", "", "Все файлы (*)"
        )
        if file_path!="":
            self.target_file_path = file_path
            self.label_before_select.setText(f"Выбранный файл: {file_path}")

    def open_settings_menu(self, _event=None):
        logging.debug('ui.MainWindow.open_settings_menu() entered')
        self.dialog = QtWidgets.QDialog()
        self.ui_settings = SettingsWindow()
        self.ui_settings.setup_ui(self.dialog)

        if self.ui_settings.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selected_option = 1 if self.ui_settings.radio_option_1.isChecked() else 2

            logging.info(f"Выбрана опция: {selected_option}")

    def save_manually(self):
        pass

    @_error_handler(FileNotFoundError, title='Ошибка конвертации', desc='Файл не выбран')
    @_error_handler(ConverterFileException, ConverterException, FileExistsError)
    def convert_file(self, _event=None):
        if not hasattr(self,'target_file_path'):
            raise FileNotFoundError('File was not selected')
        else:
            convert(self.target_file_path, self.output_file_path)
        _create_popup(title="Успех", desc=f"Файл {self.target_file_path} успешно сконвертирован и сохранен в {self.output_file_path}")
    
    def toggle_view(self, _event=None):
        logging.debug('ui.MainWindow.toggle_view() entered')
        if self.is_grayscale:
            self.is_grayscale = False
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(255, 250, 250))
            self.setPalette(palette)

            self.btn_convert_file.setStyleSheet("background-color: #FFC0CB")
            self.btn_toggle_view.setText("Версия для слабовидящих")

            logging.info('Changed into colored mode')
        else:
            self.is_grayscale = True
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(235, 235, 235))
            self.setPalette(palette)

            self.btn_convert_file.setStyleSheet("background-color: #C0C0C0")
            self.btn_toggle_view.setText("Цветная версия")

            logging.info('Changed into bw mode')

    def closeEvent(self, _event):
        logging.info("Closing...")
        self.help_window.close()
        _event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
