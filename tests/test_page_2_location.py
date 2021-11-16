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

from gui.pages.page_2_location import LocationPage
from tables.table_2_location import LocationTable
from dataimport.domeCodes import DomeCode


def test_is_complete(qtbot, tmpdir):
    table: LocationTable = LocationTable()
    locPage: LocationPage = LocationPage(table)
    qtbot.addWidget(locPage)
    locPage.show()
    qtbot.waitForWindowShown(locPage)
    assert not locPage.isComplete()

    locPage._spinLong.setValue(3.1415)
    assert table._long.content == DomeCode("3.1415", "Longitude")
    assert not locPage.isComplete()

    locPage._spinLat.setValue(2.7182)
    assert table._lat.content == DomeCode("2.7182", "Latitude")
    assert not locPage.isComplete()

    locPage._spinWaterDetpth.setValue(42.2)
    assert table._waterDepth.content == DomeCode("42.2", "Water depth", "Sounding in meters")
    assert not locPage.isComplete()

    locPage._spinMinDepth.setValue(1.1)
    assert table._minDepth.content == DomeCode("1.1", "Min Water Depth of Sample", "No furhter infos available")
    assert not locPage.isComplete()

    locPage._spinMaxDepth.setValue(2.1)
    assert table._maxDepth.content == DomeCode("2.1", "Max Water Depth of Sample", "No furhter infos available")
    assert not locPage.isComplete()

    locPage._spinPercCovered.setValue(55)
    assert table._prSub.content == DomeCode("55", "Percent covered", "Percent of bottom covered with the particular bottom substrate type")
    assert not locPage.isComplete()

    assert table._subst.content is None
    qtbot.mousePress(locPage._btnSubstrType, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(locPage._btnSubstrType._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._subst.content) == DomeCode
    assert not locPage.isComplete()

    assert table._posys.content is None
    qtbot.mousePress(locPage._btnPOSYS, QtCore.Qt.MouseButton.LeftButton)
    qtbot.mousePress(locPage._btnPOSYS._selector._btns[0], QtCore.Qt.MouseButton.LeftButton)
    assert type(table._posys.content) == DomeCode
    assert not locPage.isComplete()

    assert table._station.content is None
    locPage._lineEditStatName.setText("TestStationName")
    locPage._checkStationName()
    assert table._station.content == DomeCode("TestStationName", "Station Name", "No further information available")
    assert locPage.isComplete()

