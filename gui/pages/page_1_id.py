from PyQt6 import QtWidgets, QtCore
from typing import *
if TYPE_CHECKING:
    from tables.table_1_id import IdentificationTable

from gui.fieldSelectUI import SelectorPushButton
from dataimport.domeCodes import getLabCode, getShipCode, DomeCode
from gui.fontsAndLabels import getIsOptionalLabel, getIsMandatoryLabel


class IDPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the dataset ID.
    """
    def __init__(self, tableItem: 'IdentificationTable'):
        super(IDPage, self).__init__()
        self.setTitle("Institution Information")
        self.setSubTitle("Please enter all required information for identifying the dataset.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'IdentificationTable' = tableItem

        self._btnRLABO: SelectorPushButton = SelectorPushButton(getLabCode(),
                                                                self._tableItem.setReportingLab,
                                                                self.completeChanged)

        self._inpYEAR: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._inpYEAR.setPlaceholderText("optional: Enter in YYYY format.")
        self._inpYEAR.setToolTip("Will be created from SDATE if blank.")
        self._inpYEAR.editingFinished.connect(self._checkYearInput)

        self._btnShip: SelectorPushButton = SelectorPushButton(getShipCode(),
                                                               self._tableItem.setShipCode,
                                                               self.completeChanged)
        self._btnShip.setToolTip("""Search for "Unspecified" when ships are not used.  Minimum requirement is an "AA.." code.""")

        self._inpCruise: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._inpCruise.setPlaceholderText("Make it up if you don't go on cruises.")
        self._inpCruise.setToolTip("Make it up if you don't go on cruises - one name to be used for a year is fine.\n"
                                   "Example, use year or season if cruise number not used.")
        self._inpCruise.editingFinished.connect(self._checkCruiseInput)

        self._inpStation: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._inpStation.setPlaceholderText("Sequential number or station name")
        self._inpStation.setToolTip("Use sequential numbering or station name if unique for file.")
        self._inpStation.editingFinished.connect(self._checkStationInput)

        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Reporting Laboratory*", self._btnRLABO)
        layout.addRow("Ship/Platform Code*", self._btnShip)
        layout.addRow("Cruise Identifier*", self._inpCruise)
        layout.addRow("Station Identification / sampling event ID*", self._inpStation)
        layout.addRow(getIsOptionalLabel())
        layout.addRow("Monitoring Year", self._inpYEAR)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()

    @QtCore.pyqtSlot()
    def _checkYearInput(self) -> None:
        curText: str = self._inpYEAR.text()
        if len(curText) == 4:
            try:
                year: int = int(curText)
            except ValueError:
                QtWidgets.QMessageBox.about(self, "Invalid Year", f"'{curText}' is not a valid year input.")
            else:
                if not 1950 < year < 2025:
                    reply = QtWidgets.QMessageBox.question(self, "Continue?", f"Are you sure that the year {year} is correct?",
                                                           QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                                           QtWidgets.QMessageBox.StandardButton.Yes)
                    if reply == QtWidgets.QMessageBox.StandardButton.No:
                        return

                yearCode: DomeCode = DomeCode(curText, "Year of Entry", "")
                self._tableItem.setYear(yearCode)
        else:
            self._tableItem.setYear(None)
        self.completeChanged.emit()

    @QtCore.pyqtSlot()
    def _checkCruiseInput(self) -> None:
        curText: str = self._inpCruise.text()
        if len(curText) == 0:
            self._tableItem.setCruise(None)
        else:
            code: DomeCode = DomeCode(curText, "Cruise Description", "")
            self._tableItem.setCruise(code)
        self.completeChanged.emit()

    @QtCore.pyqtSlot()
    def _checkStationInput(self) -> None:
        curText: str = self._inpStation.text()
        if len(curText) == 0:
            self._tableItem.setStation(None)
        else:
            code: DomeCode = DomeCode(curText, "Station Description", "")
            self._tableItem.setStation(code)

        self.completeChanged.emit()
