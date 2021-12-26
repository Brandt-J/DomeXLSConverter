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
import tempfile
from typing import TYPE_CHECKING, Dict, Callable
from PyQt6 import QtCore
from unittest.mock import Mock
import random

from gui.pages.page_7_particles import ParticlesPage
from tables.table_7_particle import ParticleColumnMapping, ParticleTable
from dataimport.domeCodes import DomeCode
from dataimport.readXLS import XLSReader

if TYPE_CHECKING:
    from PyQt6 import QtWidgets
    from gui.fieldSelectUI import SelectorPushButton
    from tables.tableItem import Field
    from gui.pages.page_7_particles import CodeMapper


def test_is_complete(qtbot, tmpdir):
    def testSelectorButton(btn: 'SelectorPushButton', assignedField: 'Field'):
        assert assignedField.content is None
        qtbot.mousePress(btn, QtCore.Qt.MouseButton.LeftButton)
        btnText: str = btn._selector._btns[0].text()
        qtbot.mousePress(btn._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
        assert type(assignedField.content) == DomeCode
        assert assignedField.content.code == btnText
        qtbot.mousePress(btn._selector._btnReset, QtCore.Qt.MouseButton.LeftButton)
        assert assignedField.content is None
        qtbot.mousePress(btn._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
        assert type(assignedField.content) == DomeCode
        assert assignedField.content.code == btnText

    def testMappingButton(btn: 'QtWidgets.QPushButton', codeMapper: 'CodeMapper',
                          getAssignedDictFunc: Callable[[], Dict[str, 'DomeCode']]):
        assert len(getAssignedDictFunc()) == 0
        qtbot.mousePress(btn, QtCore.Qt.MouseButton.LeftButton)  # Opens the CodeMapper
        qtbot.waitForWindowShown(codeMapper)
        assert len(codeMapper._btns) > 0
        expectedDict: Dict[str, 'DomeCode'] = {}
        for lbl, btn in zip(codeMapper._lbls, codeMapper._btns):
            qtbot.mousePress(btn, QtCore.Qt.MouseButton.LeftButton)  # Opens the CodeSelector
            numEntries: int = len(btn._selector._btns)
            randBtnInd: int = random.randint(0, numEntries-1)
            qtbot.mousePress(btn._selector._btns[randBtnInd], QtCore.Qt.MouseButton.LeftButton)
            expectedDict[lbl.text()] = btn._selector._codes[randBtnInd]
        qtbot.mousePress(codeMapper._btnAccept, QtCore.Qt.MouseButton.LeftButton)
        assert getAssignedDictFunc() == expectedDict

    def failFunc():
        raise AssertionError

    table: ParticleColumnMapping = ParticleColumnMapping()
    createDFrameMock: Mock = Mock()

    if os.getcwd().endswith("tests"):
        os.chdir(os.path.dirname(os.getcwd()))

    xlsReader: XLSReader = XLSReader()
    xlsReader.readXlsFile(r"data\exampledata.xlsx")
    xlsReader.setActiveSheet("p3 unprocessed")

    page: ParticlesPage = ParticlesPage(table, createDFrameMock, xlsReader)
    page.setupToAvailableColumns()

    qtbot.addWidget(page)
    page.show()
    qtbot.waitForWindowShown(page)
    assert not page.isComplete()

    assert not page._btnMapString2Color.isEnabled()
    testSelectorButton(page._btnColor, table._colorColumn)
    assert not page.isComplete()
    assert page._btnMapString2Color.isEnabled()

    assert not page._btnMapString2Type.isEnabled()
    testSelectorButton(page._btnType, table._polymTypeColumn)
    assert not page.isComplete()
    assert page._btnMapString2Type.isEnabled()

    assert not page._btnMapString2Shape.isEnabled()
    testSelectorButton(page._btnShape, table._shapeColumn)
    assert not page.isComplete()
    assert page._btnMapString2Shape.isEnabled()

    testSelectorButton(page._btnSize, table._sizeColumn)
    assert not page.isComplete()

    testMappingButton(page._btnMapString2Type, page._codeMapper, table.getTypeMapping)
    testMappingButton(page._btnMapString2Color, page._codeMapper, table.getColorMapping)
    testMappingButton(page._btnMapString2Shape, page._codeMapper, table.getShapeMapping)

    with tempfile.TemporaryDirectory() as tmpDirName:
        resultFileName: str = os.path.join(tmpDirName, "testExport.xlsx")
        page._getSaveFileName = lambda: resultFileName
        success: bool = page.validatePage()  # i.e., click "Finish"
        assert success
        createDFrameMock.assert_called_once()

        page._createDFrameFunc = failFunc
        success: bool = page.validatePage()  # i.e., click "Finish" again
        assert not success


def test_getParticleSize(qtbot, tmpdir):
    partTable: ParticleTable = ParticleTable()
    assert partTable._getSizeCodeOfSize(50) == DomeCode("30", "micron <=100 um")
    assert partTable._getSizeCodeOfSize(100) == DomeCode("30", "micron <=100 um")
    assert partTable._getSizeCodeOfSize(5) == DomeCode("30", "micron <=100 um")

    assert partTable._getSizeCodeOfSize(101) == DomeCode("31", "micron 101-200 um")
    assert partTable._getSizeCodeOfSize(150) == DomeCode("31", "micron 101-200 um")
    assert partTable._getSizeCodeOfSize(200) == DomeCode("31", "micron 101-200 um")

    assert partTable._getSizeCodeOfSize(201) == DomeCode("32", "micron 201-300 um")
    assert partTable._getSizeCodeOfSize(250) == DomeCode("32", "micron 201-300 um")
    assert partTable._getSizeCodeOfSize(300) == DomeCode("32", "micron 201-300 um")

    assert partTable._getSizeCodeOfSize(301) == DomeCode("33", "micron 301-400 um")
    assert partTable._getSizeCodeOfSize(350) == DomeCode("33", "micron 301-400 um")
    assert partTable._getSizeCodeOfSize(400) == DomeCode("33", "micron 301-400 um")

    assert partTable._getSizeCodeOfSize(401) == DomeCode("34", "micron 401-500 um")
    assert partTable._getSizeCodeOfSize(400.902) == DomeCode("34", "micron 401-500 um")
    assert partTable._getSizeCodeOfSize(450) == DomeCode("34", "micron 401-500 um")
    assert partTable._getSizeCodeOfSize(500) == DomeCode("34", "micron 401-500 um")

    assert partTable._getSizeCodeOfSize(501) == DomeCode("35", "micron 501-1000 um")
    assert partTable._getSizeCodeOfSize(750) == DomeCode("35", "micron 501-1000 um")
    assert partTable._getSizeCodeOfSize(1000) == DomeCode("35", "micron 501-1000 um")

    assert partTable._getSizeCodeOfSize(2000) == DomeCode("5", "mm 1.0-2.79 mm")
    assert partTable._getSizeCodeOfSize(5500) == DomeCode("8", "cm 0.5-0.99 cm")
