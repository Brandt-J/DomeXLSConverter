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
                             DomeCode("Code2", "Another Description", "None")]
    selPushBtn: SelectorPushButton = SelectorPushButton(codes, addEmittedCode)
    qtbot.addWidget(selPushBtn)

    for i, code in enumerate(codes):
        assert selPushBtn._selector.isHidden()
        qtbot.mousePress(selPushBtn, Qt.MouseButton.LeftButton)
        assert selPushBtn._selector.isVisible()

        qtbot.mousePress(selPushBtn._selector._btns[i], Qt.MouseButton.LeftButton)
        assert len(emittedCodes) == i+1
        assert code in emittedCodes
