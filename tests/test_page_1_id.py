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


from PyQt6 import QtCore

from gui.pages.page_1_id import IDPage
from tables.table_1_id import IdentificationTable
from dataimport.domeCodes import DomeCode


def test_is_complete(qtbot, tmpdir):
    table: IdentificationTable = IdentificationTable()
    idPage: IDPage = IDPage(table)
    qtbot.addWidget(idPage)
    idPage.show()
    qtbot.waitForWindowShown(idPage)
    assert not idPage.isComplete()

    assert table._lab.content is None
    qtbot.mousePress(idPage._btnRLABO, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(idPage._btnRLABO._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._lab.content) == DomeCode
    assert not idPage.isComplete()

    assert table._year.content is None
    idPage._inpYEAR.setText("12345")
    idPage._checkYearInput()
    assert table._year.content is None
    idPage._inpYEAR.setText("Gar keine Zahl")
    idPage._checkYearInput()
    assert table._year.content is None
    idPage._inpYEAR.setText("2015")
    idPage._checkYearInput()
    assert type(table._year.content) == DomeCode
    assert table._year.content.code == "2015"
    assert not idPage.isComplete()
    idPage._inpYEAR.setText("")
    idPage._checkYearInput()
    assert table._year.content is None
    idPage._inpYEAR.setText("2018")
    idPage._checkYearInput()
    assert type(table._year.content) == DomeCode
    assert table._year.content.code == "2018"
    assert not idPage.isComplete()

    assert table._cruise.content is None
    idPage._inpCruise.setText("FakeName")
    idPage._checkCruiseInput()
    assert type(table._cruise.content) == DomeCode
    assert table._cruise.content.code == "FakeName"
    idPage._inpCruise.setText("")
    idPage._checkCruiseInput()
    assert table._cruise.content is None
    idPage._inpCruise.setText("FakeName2")
    idPage._checkCruiseInput()
    assert type(table._cruise.content) == DomeCode
    assert table._cruise.content.code == "FakeName2"
    assert not idPage.isComplete()

    assert table._ship.content is None
    qtbot.mousePress(idPage._btnShip, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(idPage._btnShip._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._ship.content) == DomeCode
    assert not idPage.isComplete()

    assert table._station.content is None
    idPage._inpStation.setText("FakeName")
    idPage._checkStationInput()
    assert type(table._station.content) == DomeCode
    assert table._station.content.code == "FakeName"
    idPage._inpStation.setText("")
    idPage._checkStationInput()
    assert table._station.content is None
    idPage._inpStation.setText("FakeName2")
    idPage._checkStationInput()
    assert type(table._station.content) == DomeCode
    assert table._station.content.code == "FakeName2"

    assert idPage.isComplete()

