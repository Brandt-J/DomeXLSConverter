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
from unittest.mock import Mock
from PyQt6.QtCore import Qt

from gui.fieldSelectUI import SelectorPushButton
from dataimport.domeCodes import DomeCode


def test_fieldSelectorButton(qtbot, tmpdir, mocker):
    emittedCodes: List[DomeCode] = []

    def addEmittedCode(emittedCode: DomeCode) -> None:
        emittedCodes.append(emittedCode)

    callFunc: Mock = mocker.Mock()
    codes: List[DomeCode] = [DomeCode("Code1", "Description", "Loooong Description"),
                             DomeCode("Code2", "Another Description")]
    selPushBtn: SelectorPushButton = SelectorPushButton(codes, addEmittedCode)
    qtbot.addWidget(selPushBtn)

    for i, code in enumerate(codes):
        assert selPushBtn._selector.isHidden()
        qtbot.mousePress(selPushBtn, Qt.MouseButton.LeftButton)
        assert selPushBtn._selector.isVisible()

        qtbot.mousePress(selPushBtn._selector._btns[i], Qt.MouseButton.LeftButton)
        assert len(emittedCodes) == i+1
        assert code in emittedCodes
