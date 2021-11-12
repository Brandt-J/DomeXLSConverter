import os
from PyQt6 import QtCore

from dataimport.readXLS import XLSReader
from gui.pages.page_0_intro import IntroPage


def test_is_complete(qtbot, tmpdir):
    introPage: IntroPage = IntroPage(XLSReader())
    qtbot.addWidget(introPage)
    introPage.show()
    qtbot.waitForWindowShown(introPage)
    assert not introPage.isComplete()

    introPage._getXLSFileName = lambda: r"data\exampledata.xlsx"  # now take a valid file
    assert os.path.exists(introPage._getXLSFileName())
    qtbot.mousePress(introPage._btnLoadXLS, QtCore.Qt.MouseButton.LeftButton)
    assert introPage._xlsLoaded
    assert len(introPage._xlsReader._activeSheet) > 0

    assert introPage.isComplete()
