from PyQt6 import QtWidgets, QtGui
import sys
import os
from frontend.ui import MainWindow

app = QtWidgets.QApplication(sys.argv)

ICON_FILE_PATH=os.path.join(os.path.dirname(__file__), 'Orca.svg')
app.setWindowIcon(QtGui.QIcon(ICON_FILE_PATH))


window = MainWindow()
window.show()
sys.exit(app.exec())