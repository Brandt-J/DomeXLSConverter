from PyQt6 import QtWidgets, QtCore
from typing import *

from gui.fieldSelectUI import SelectorPushButton
from dataimport.domeCodes import DomeCode, getPositioningSystems, getSubstrateTypes
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel

if TYPE_CHECKING:
    from tables.table_2_location import LocationTable


class LocationPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the dataset ID.
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
                                   "</a>, enter the 'Station_Code')")
        self._statNameInfo.setOpenExternalLinks(True)

        self._spinWaterDetpth: QtWidgets.QDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self._spinMinDepth: QtWidgets.QDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        self._spinMaxDepth: QtWidgets.QDoubleSpinBox = QtWidgets.QDoubleSpinBox()
        for spinbox in [self._spinWaterDetpth, self._spinMinDepth, self._spinMaxDepth]:
            spinbox.setMinimum(0)
            spinbox.setMaximum(1e5)
            spinbox.setDecimals(1)
            spinbox.setValue(30.0)
            spinbox.setMaximumWidth(self.spinboxwidth)

        self._spinWaterDetpth.valueChanged.connect(self._tableItem.setWaterDepth)
        self._spinMinDepth.valueChanged.connect(self._tableItem.setMinDepth)
        self._spinMaxDepth.valueChanged.connect(self._tableItem.setMaxDepth)

        self._btnSubstrType: SelectorPushButton = SelectorPushButton(getSubstrateTypes(), self._tableItem.setSubstrateType,
                                                                     self.completeChanged)
        self._spinPercCovered: QtWidgets.QSpinBox = QtWidgets.QSpinBox()
        self._spinPercCovered.setMinimum(0)
        self._spinPercCovered.setMaximum(100)
        self._spinPercCovered.setFixedWidth(self.spinboxwidth)
        self._spinPercCovered.valueChanged.connect(self._tableItem.setPercentCovered)
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