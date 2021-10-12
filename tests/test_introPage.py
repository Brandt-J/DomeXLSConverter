import os
from PyQt6 import QtCore

from gui.pages.introPage import IntroPage

os.chdir(os.path.dirname(os.getcwd()))  # to make loading the test xs file possible


def test_is_complete(qtbot, tmpdir):
    introPage: IntroPage = IntroPage()
    qtbot.addWidget(introPage)
    introPage.show()
    qtbot.waitForWindowShown(introPage)
    assert not introPage.isComplete()

    introPage._getXLSFileName = lambda: r"data\exampledata.xlsx"  # now take a valid file
    assert os.path.exists(introPage._getXLSFileName())
    qtbot.mousePress(introPage._btnLoadXLS, QtCore.Qt.MouseButton.LeftButton)
    assert introPage._xlsLoaded

    qtbot.mousePress(introPage._btnConnectDB, QtCore.Qt.MouseButton.LeftButton)
    assert introPage._dbConnected
    assert introPage.isComplete()
