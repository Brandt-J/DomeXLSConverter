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


from typing import *
from PyQt6.QtCore import Qt

from gui.fieldSelectUI import SelectorPushButton
from dataimport.domeCodes import DomeCode


def test_fieldSelectorButton(qtbot, tmpdir):
    emittedCodes: List[DomeCode] = []

    def addEmittedCode(emittedCode: DomeCode) -> None:
        emittedCodes.append(emittedCode)

    codes: List[DomeCode] = [DomeCode("Code1", "Description", "Loooong Description"),
                             DomeCode("Code2", "Another Description")]
    selPushBtn: SelectorPushButton = SelectorPushButton(codes, addEmittedCode)
    qtbot.addWidget(selPushBtn)

    for i, code in enumerate(codes):
        qtbot.mousePress(selPushBtn, Qt.MouseButton.LeftButton)

        qtbot.mousePress(selPushBtn._selector._btns[i], Qt.MouseButton.LeftButton)
        assert len(emittedCodes) == i+1
        assert code in emittedCodes

    numCodes: int = len(emittedCodes)
    qtbot.mousePress(selPushBtn._selector._btnReset, Qt.MouseButton.LeftButton)
    assert len(emittedCodes) == numCodes + 1
    assert emittedCodes[-1] is None
