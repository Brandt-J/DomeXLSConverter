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
from typing import TYPE_CHECKING
from PyQt6 import QtCore

from gui.pages.page_5_analysis import AnalysisPage
from tables.table_5_analysis import AnalysisTable

from dataimport.domeCodes import DomeCode
if TYPE_CHECKING:
    from gui.fieldSelectUI import SelectorPushButton
    from tables.tableItem import Field


def test_is_complete(qtbot, tmpdir):
    def testSelectorButton(btn: 'SelectorPushButton', assignedField: 'Field'):
        assert assignedField.content is None
        qtbot.mousePress(btn, QtCore.Qt.MouseButton.LeftButton)
        qtbot.mousePress(btn._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
        assert type(assignedField.content) == DomeCode
        qtbot.mousePress(btn._selector._btnReset, QtCore.Qt.MouseButton.LeftButton)
        assert assignedField.content is None
        qtbot.mousePress(btn._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
        assert type(assignedField.content) == DomeCode

    table: AnalysisTable = AnalysisTable()
    page: AnalysisPage = AnalysisPage(table)
    qtbot.addWidget(page)
    page.show()
    qtbot.waitForWindowShown(page)
    assert not page.isComplete()

    # testSelectorButton(page._btnLitRef, table._ltref)  # reenable these lines if the litter-reference is again in the UI
    # assert not page.isComplete()

    testSelectorButton(page._btnAnaltyicLab, table._alabo)
    assert not page.isComplete()

    testSelectorButton(page._btnRefSource, table._refsk)
    assert not page.isComplete()

    testSelectorButton(page._btnMethPuri, table._metps)
    assert not page.isComplete()

    testSelectorButton(page._btnMethPretreat, table._metpt)
    assert not page.isComplete()

    testSelectorButton(page._btnMethAnal, table._metoa)
    assert page.isComplete()

