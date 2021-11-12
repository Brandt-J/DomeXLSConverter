"""
DomeExcelConverter
Copyright (C) 2021 Josef Brandt, University of Gothenburg <josef.brandt@gu.se>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program, see COPYING.
If not, see <https://www.gnu.org/licenses/>.
"""


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
