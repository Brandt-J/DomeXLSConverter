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
from typing import TYPE_CHECKING, Union, Callable
from PyQt6 import QtCore

from gui.pages.page_4_sample import SamplePage
from tables.table_4_sample import SampleTable

from dataimport.domeCodes import DomeCode
if TYPE_CHECKING:
    from gui.checkableWidget import CheckableSpinBox, CheckableDoubleSpinBox
    from tables.tableItem import Field


def test_is_complete(qtbot, tmpdir):
    def testCheckableSpinbox(spinbox: Union['CheckableSpinBox', 'CheckableDoubleSpinBox'],
                             updateFn: Union[Callable[[bool, float], None], Callable[[bool, int], None]],
                             fieldToSet: 'Field',
                             expectedCodeDescr: str) -> None:
        assert fieldToSet.content is None
        spinbox.setChecked(False)
        spinbox.setValue(5)
        updateFn(spinbox.isChecked(), spinbox.getValue())
        assert fieldToSet.content is None

        spinbox.setChecked(True)
        updateFn(spinbox.isChecked(), spinbox.getValue())
        assert fieldToSet.content == DomeCode("5", expectedCodeDescr)

        spinbox.setValue(6)
        updateFn(spinbox.isChecked(), spinbox.getValue())
        assert fieldToSet.content == DomeCode("6", expectedCodeDescr)

    table: SampleTable = SampleTable()
    page: SamplePage = SamplePage(table)
    qtbot.addWidget(page)
    page.show()
    qtbot.waitForWindowShown(page)
    assert not page.isComplete()

    assert table._dtype.content is None
    qtbot.mousePress(page._btnDType, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(page._btnDType._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._dtype.content) == DomeCode
    assert not page.isComplete()

    page._editSampleNo.setText("")
    page._sampleNumberChanged()
    assert table._smpno.content is None
    assert not page.isComplete()

    page._editSampleNo.setText("Sample 1")
    page._sampleNumberChanged()
    assert table._smpno.content == DomeCode("Sample 1", "Sample Number")
    assert not page.isComplete()

    assert table._finfl.content is None
    qtbot.mousePress(page._btnInfFac, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(page._btnInfFac._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._finfl.content) == DomeCode
    assert not page.isComplete()

    testCheckableSpinbox(page._spinNoAgg, page._noAggChanged, table._noagg, "Number of aggregated Samples")
    assert not page.isComplete()

    testCheckableSpinbox(page._spinSubNo, page._subNoChanged, table._subno, "Subsample Number")
    assert not page.isComplete()

    assert table._matrx.content is None
    qtbot.mousePress(page._btnMatrix, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(page._btnMatrix._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._matrx.content) == DomeCode
    assert page.isComplete()

