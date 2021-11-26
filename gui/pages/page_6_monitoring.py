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

from dataimport.domeCodes import getMonitoringPurposes, getMonitoringProgrammes
from gui.fontsAndLabels import getIsMandatoryLabel
from gui.fieldSelectUI import SelectorPushButton

if TYPE_CHECKING:
    from tables.table_6_monitoring import MonitoringTable


class MonitoringPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about monitoring programme and purpose.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'MonitoringTable'):
        super(MonitoringPage, self).__init__()
        self.setTitle("Monitoring Campaing Information")
        self.setSubTitle("Please enter all required information about the monitoring campaing.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'MonitoringTable' = tableItem

        self._btnPurpose: SelectorPushButton = SelectorPushButton(getMonitoringPurposes(), self._tableItem.setMonitoringPurpose,
                                                                   self.completeChanged, allowMultiSelect=True)
        self._btnProgramme: SelectorPushButton = SelectorPushButton(getMonitoringProgrammes(), self._tableItem.setProgramme,
                                                                   self.completeChanged, allowMultiSelect=True)
        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Purpose(s) of Monitoring:*", self._btnPurpose)
        layout.addRow("Monitoring Programme(s):*", self._btnProgramme)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()
