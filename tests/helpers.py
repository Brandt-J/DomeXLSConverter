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

from dataimport.domeCodes import DomeCode
if TYPE_CHECKING:
    from gui.checkableWidget import CheckableSpinBox, CheckableDoubleSpinBox
    from tables.tableItem import Field


def testCheckableSpinbox(spinbox: Union['CheckableSpinBox', 'CheckableDoubleSpinBox'],
                         updateFn: Union[Callable[[bool, float], None], Callable[[bool, int], None]],
                         fieldToSet:'Field',
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

