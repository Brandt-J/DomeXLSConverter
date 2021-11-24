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

from dataimport.domeCodes import getRefSources, getPretreatments, getPurifications, getAnalyses
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel
from gui.fieldSelectUI import SelectorPushButton

if TYPE_CHECKING:
    from tables.table_5_analysis import AnalysisTable


class AnalysisPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about pretreatment and analysis.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'AnalysisTable'):
        super(AnalysisPage, self).__init__()
        self.setTitle("Analysis Information")
        self.setSubTitle("Please enter all required information about sample pretreatment and analysis.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'AnalysisTable' = tableItem

        self._btnRefSource: SelectorPushButton = SelectorPushButton(getRefSources(), self._tableItem.setRefSource,
                                                                   self.completeChanged)
        self._btnMethPretreat: SelectorPushButton = SelectorPushButton(getPretreatments(), self._tableItem.setMethPretreat,
                                                                   self.completeChanged, allowMultiSelect=True)
        self._btnMethPuri: SelectorPushButton = SelectorPushButton(getPurifications(), self._tableItem.setMethodPurification,
                                                                   self.completeChanged)
        self._btnMethAnal: SelectorPushButton = SelectorPushButton(getAnalyses(), self._tableItem.setMethodAnalysis,
                                                                   self.completeChanged)
        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Pretreatment:*", self._btnMethPretreat)
        layout.addRow("Purification/Separation:*", self._btnMethPuri)
        layout.addRow("Analysis:*", self._btnMethAnal)
        layout.addRow(getIsOptionalLabel())
        layout.addRow("Reference Source or key:", self._btnRefSource)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()
