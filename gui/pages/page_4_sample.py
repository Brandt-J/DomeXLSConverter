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

from dataimport.domeCodes import DomeCode, getSampleDTypes, getInfluencingFactors, getMatrices
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel
from gui.fieldSelectUI import SelectorPushButton
from gui.checkableWidget import CheckableSpinBox

if TYPE_CHECKING:
    from tables.table_4_sample import SampleTable


class SamplePage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the dataset ID.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'SampleTable'):
        super(SamplePage, self).__init__()
        self.setTitle("Sample Information")
        self.setSubTitle("Please enter all required information about when the sample itself.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'SampleTable' = tableItem

        self._btnDType: SelectorPushButton = SelectorPushButton(getSampleDTypes(), self._tableItem.setDType,
                                                                self.completeChanged)
        self._editSampleNo: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._editSampleNo.setPlaceholderText("Any character 0–9, A–Z etc.")
        self._editSampleNo.setToolTip("Sample number / Sample identification for haul or group of individuals/cores/bottles collected at that time/place")
        self._editSampleNo.textChanged.connect(self._sampleNumberChanged)
        self._btnInfFac: SelectorPushButton = SelectorPushButton(getInfluencingFactors(), self._tableItem.setInfluencingFactors,
                                                                 self.completeChanged)
        self._btnMatrix: SelectorPushButton = SelectorPushButton(getMatrices(), self._tableItem.setMatrix,
                                                                 self.completeChanged)

        self._spinNoAgg: CheckableSpinBox = CheckableSpinBox()
        self._spinNoAgg.Changed.connect(self._noAggChanged)
        self._spinNoAgg.setMinimum(2)
        self._spinNoAgg.setMaximum(99)
        self._spinNoAgg.setMaximumWidth(self.elementWidth)
        self._spinNoAgg.setToolTip("Number of subsamples combined if sample is an aggregation.\n"
                                   "On beach where multiple people have sampled but the items are combined, this can be an option")

        self._spinSubNo: CheckableSpinBox = CheckableSpinBox()
        self._spinSubNo.setMinimum(1)
        self._spinSubNo.setMaximum(100)
        self._spinSubNo.setMaximum(self.elementWidth)
        self._spinSubNo.Changed.connect(self._subNoChanged)

        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Data Type:*", self._btnDType)
        layout.addRow("Sample Number:*", self._editSampleNo)
        layout.addRow("Sample Matrix:*", self._btnMatrix)
        layout.addRow(getIsOptionalLabel())
        layout.addRow("Influencing Factors:", self._btnInfFac)
        layout.addRow("Number aggreg. samples:", self._spinNoAgg)
        layout.addRow("Subsample Number:", self._spinSubNo)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()

    @QtCore.pyqtSlot(bool, int)
    def _noAggChanged(self, checked: bool, num: int) -> None:
        if checked and 2 <= num <= 99:
            self._tableItem.setNumberAggregations(DomeCode(str(num), "Number of aggregated Samples"))
        else:
            self._tableItem.setNumberAggregations(None)

    @QtCore.pyqtSlot(bool, int)
    def _subNoChanged(self, checked: bool, num: int) -> None:
        if checked:
            self._tableItem.setSubsampleNumber(DomeCode(str(num), "Subsample Number"))
        else:
            self._tableItem.setNumberAggregations(None)

    def _sampleNumberChanged(self) -> None:
        text: str = self._editSampleNo.text()
        if text:
            self._tableItem.setSampleNumber(DomeCode(text, "Sample Number"))
        else:
            self._tableItem.setSampleNumber(None)
