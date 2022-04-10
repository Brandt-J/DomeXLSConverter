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


from PyQt6 import QtWidgets, QtCore
from typing import *

from gui.fieldSelectUI import SelectorPushButton
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel
from gui.checkableWidget import CheckableDoubleSpinBox, CheckableSpinBox
from dataimport.domeCodes import DomeCode, getPositioningSystems, getSubstrateTypes

if TYPE_CHECKING:
    from tables.table_2_location import LocationTable


class LocationPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the sample location.
    """
    spinboxwidth: int = 100

    def __init__(self, tableItem: 'LocationTable'):
        super(LocationPage, self).__init__()
        self.setTitle("Sample Location")
        self.setSubTitle("Please enter all required information about where the sample was taken.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'LocationTable' = tableItem
        self._spinLong: QtWidgets.QDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self._spinLong.setMinimum(-180.0)
        self._spinLong.setMaximum(180.0)
        self._spinLong.setValue(11.2760)
        self._spinLong.valueChanged.connect(self._tableItem.setLongitude)

        self._spinLat: QtWidgets.QDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self._spinLat.setMinimum(-90.0)
        self._spinLat.setMaximum(90.0)
        self._spinLat.setValue(58.1460)
        self._spinLat.valueChanged.connect(self._tableItem.setLatitude)

        for spinbox in [self._spinLat, self._spinLong]:
            spinbox.setDecimals(4)
            spinbox.setMaximumWidth(self.spinboxwidth)

        self._tableItem.setLongitude(self._spinLong.value())
        self._tableItem.setLatitude(self._spinLat.value())

        self._btnPOSYS: SelectorPushButton = SelectorPushButton(getPositioningSystems(), self._tableItem.setPosSystem,
                                                                self.completeChanged)
        self._lineEditStatName: QtWidgets.QLineEdit = QtWidgets.QLineEdit(self)
        self._lineEditStatName.editingFinished.connect(self._checkStationName)
        self._lineEditStatName.setPlaceholderText("""Any character 0–9 or A–Z. No ";" or "," or double spaces or parenthesis.""")
        self._statNameInfo: QtWidgets.QLabel = QtWidgets.QLabel()
        self._statNameInfo.setText("<a style='text-decoration:underline;color:black'href='https://gis.ices.dk/sf/index.html?widget=station'>"
                                   "(Click Here to browse"
                                   "</a>, enter the 'Station_Name')")
        self._statNameInfo.setOpenExternalLinks(True)

        self._spinWaterDetpth: CheckableDoubleSpinBox = CheckableDoubleSpinBox()
        self._spinMinDepth: CheckableDoubleSpinBox = CheckableDoubleSpinBox()
        self._spinMaxDepth: CheckableDoubleSpinBox = CheckableDoubleSpinBox()
        for spinbox in [self._spinWaterDetpth, self._spinMinDepth, self._spinMaxDepth]:
            spinbox.setMinimum(0)
            spinbox.setMaximum(1e5)
            spinbox.setDecimals(1)
            spinbox.setValue(30.0)
            spinbox.setMaximumWidth(self.spinboxwidth)

        self._spinWaterDetpth.Changed.connect(self._waterDepthChanged)
        self._spinMinDepth.Changed.connect(self._minDepthChanged)
        self._spinMaxDepth.Changed.connect(self._maxDepthChanged)

        self._btnSubstrType: SelectorPushButton = SelectorPushButton(getSubstrateTypes(), self._tableItem.setSubstrateType,
                                                                     self.completeChanged)
        self._spinPercCovered: CheckableSpinBox = CheckableSpinBox()
        self._spinPercCovered.setMinimum(0)
        self._spinPercCovered.setMaximum(100)
        self._spinPercCovered.setMaximumWidth(self.spinboxwidth)
        self._spinPercCovered.Changed.connect(self._percCoveredChanged)
        self._spinPercCovered.setToolTip("Percent of bottom covered with the particular bottom substrate type")

        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Longitude*", self._spinLong)
        layout.addRow("Latitude*", self._spinLat)
        layout.addRow("Station name*", self._lineEditStatName)
        layout.addRow(self._statNameInfo)

        layout.addRow(getIsOptionalLabel())
        layout.addRow("Positioning system", self._btnPOSYS)
        layout.addRow("Water depth (m)", self._spinWaterDetpth)
        layout.addRow("Minimum depth of sample (m)", self._spinMinDepth)
        layout.addRow("Maximum depth of sample (m)", self._spinMaxDepth)
        layout.addRow("Bottom substrate type", self._btnSubstrType)
        layout.addRow("Percent covered", self._spinPercCovered)

    @QtCore.pyqtSlot()
    def _checkStationName(self) -> None:

        curText: str = self._lineEditStatName.text()
        if len(curText) == 0:
            self._tableItem.setStationName(None)
        else:
            code: DomeCode = DomeCode(curText, "Station Name", "No further information available")
            self._tableItem.setStationName(code)

        self.completeChanged.emit()

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()

    @QtCore.pyqtSlot(bool, float)
    def _waterDepthChanged(self, checked: bool, depth: float) -> None:
        if checked:
            self._tableItem.setWaterDepth(DomeCode(str(depth), "Water depth", "Sounding in meters"))
        else:
            self._tableItem.setWaterDepth(None)

    @QtCore.pyqtSlot(bool, float)
    def _minDepthChanged(self, checked: bool, minDepth: float) -> None:
        if checked:
            self._tableItem.setMinDepth(DomeCode(str(minDepth), "Min Water Depth of Sample"))
        else:
            self._tableItem.setMinDepth(None)

    @QtCore.pyqtSlot(bool, float)
    def _maxDepthChanged(self, checked: bool, maxDepth: float) -> None:
        if checked:
            self._tableItem.setMaxDepth(DomeCode(str(maxDepth), "Max Water Depth of Sample"))
        else:
            self._tableItem.setMaxDepth(None)

    @QtCore.pyqtSlot(bool, int)
    def _percCoveredChanged(self, checked: bool, percCovered: int) -> None:
        if checked:
            self._tableItem.setPercentCovered(DomeCode(str(percCovered), "Percent covered",
                                                       "Percent of bottom covered with the particular bottom substrate type"))
        else:
            self._tableItem.setPercentCovered(None)
