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

from gui.pages.page_6_particles import ParticlesPage
from tables.table_6_particle import ParticleColumnAssignments

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

    table: ParticleColumnAssignments = ParticleColumnAssignments()
    page: ParticlesPage = ParticlesPage(table)
    page.setupToAvailableColumns(["col1", "col2", "col3"])
    qtbot.addWidget(page)
    page.show()
    qtbot.waitForWindowShown(page)
    assert not page.isComplete()

    testSelectorButton(page._btnColor, table._colorColumn)
    assert not page.isComplete()

    testSelectorButton(page._btnType, table._polymTypeColumn)
    assert not page.isComplete()

    testSelectorButton(page._btnShape, table._shapeColumn)
    assert not page.isComplete()

    testSelectorButton(page._btnSize, table._sizeColumn)
    assert page.isComplete()

