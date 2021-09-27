from PyQt6 import QtWidgets
import sys

from gui.schemeView import SchemeView


class MainWindow(QtWidgets.QMainWindow):
    """
    Main Window of the application.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self._schemeView: SchemeView = SchemeView()
        self.setCentralWidget(self._schemeView)


if __name__ == '__main__':
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    mainWin: MainWindow = MainWindow()
    mainWin.show()
    app.exec()
