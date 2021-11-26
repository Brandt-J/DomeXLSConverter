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

from PyQt6 import QtWidgets
from typing import *

from dataimport.domeCodes import DomeCode
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel
from gui.fieldSelectUI import SelectorPushButton

if TYPE_CHECKING:
    from tables.table_6_particle import ParticleColumnAssignments


class ParticlesPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the particles.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'ParticleColumnAssignments'):
        super(ParticlesPage, self).__init__()
        self.setTitle("Analysis Information")
        self.setSubTitle("Please select which columns from the excel sheet to use for which database field.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'ParticleColumnAssignments' = tableItem
        self.setButtonText(QtWidgets.QWizard.WizardButton.FinishButton,
                           "Create And Save Litter Report File")

        self._btnShape: Union[None, SelectorPushButton] = None
        self._btnSize: Union[None, SelectorPushButton] = None
        self._btnType: Union[None, SelectorPushButton] = None
        self._btnColor: Union[None, SelectorPushButton] = None

    def setupToAvailableColumns(self, availableColumns: List[str]) -> None:
        columnNameCodes: List[DomeCode] = [DomeCode(name, "FakeCode") for name in availableColumns]

        self._btnShape = SelectorPushButton(columnNameCodes, self._tableItem.setShapeColumn, self.completeChanged,
                                            hideDescriptions=True)
        self._btnSize = SelectorPushButton(columnNameCodes, self._tableItem.setSizeColumn, self.completeChanged,
                                           hideDescriptions=True)
        self._btnType = SelectorPushButton(columnNameCodes, self._tableItem.setPolymTypeColumn, self.completeChanged,
                                           hideDescriptions=True)
        self._btnColor = SelectorPushButton(columnNameCodes, self._tableItem.setColorColumn, self.completeChanged,
                                            hideDescriptions=True)

        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Column Particle Size", self._btnSize)
        layout.addRow(getIsOptionalLabel())
        layout.addRow("Column Polymer Type", self._btnType)
        layout.addRow("Column Particle Shape", self._btnShape)
        layout.addRow("Column Particle Color", self._btnColor)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()

