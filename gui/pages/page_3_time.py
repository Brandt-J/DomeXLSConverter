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

from dataimport.domeCodes import DomeCode
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel

if TYPE_CHECKING:
    from tables.table_3_time import TimeTable


def QDate2String(date: QtCore.QDate) -> str:
    day: str = str(date.day())
    while len(day) < 2:
        day = "0"+day
    month: str = str(date.month())
    while len(month) < 2:
        month = "0"+month
    year: str = str(date.year())
    return year + month + day


def QTime2String(time: QtCore.QTime) -> str:
    hours: str = str(time.hour())
    while len(hours) < 2:
        hours = "0"+hours
    minutes: str = str(time.minute())
    while len(minutes) < 2:
        minutes = "0"+minutes
    return hours + minutes


class TimePage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the sampling time.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'TimeTable'):
        super(TimePage, self).__init__()
        self.setTitle("Sample Time")
        self.setSubTitle("Please enter all required information about when the sample was taken.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'TimeTable' = tableItem

        self._sampleDateEdit: QtWidgets.QDateEdit = QtWidgets.QDateEdit()
        self._sampleDateEdit.setFixedWidth(self.elementWidth)
        self._sampleDateEdit.setDisplayFormat("dd.MM.yyyy")
        self._sampleDateEdit.setDate(QtCore.QDate.currentDate())
        self._sampleDateEdit.dateChanged.connect(self._updateSamplingDate)
        self._updateSamplingDate()

        self._sampleEndDateEdit: QtWidgets.QDateEdit = QtWidgets.QDateEdit()
        self._sampleEndDateEdit.setFixedWidth(self.elementWidth)
        self._sampleEndDateEdit.setDisplayFormat("dd.MM.yyyy")
        self._sampleEndDateEdit.setDate(QtCore.QDate.currentDate())
        self._sampleEndDateEdit.dateChanged.connect(self._updateSamplingEndDate)
        self._sampleEndDateEdit.setEnabled(False)
        self._checkSampleEndDate: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Include")
        self._checkSampleEndDate.toggled.connect(self._toggleSampleEndDate)

        self._samplingTimeEdit: QtWidgets.QTimeEdit = QtWidgets.QTimeEdit()
        self._samplingTimeEdit.timeChanged.connect(self._updateSamplingTime)
        self._checkSamplingTime: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Include")
        self._checkSamplingTime.toggled.connect(self._toggleSamplingTime)

        self._actualTimeEdit: QtWidgets.QTimeEdit = QtWidgets.QTimeEdit()
        self._actualTimeEdit.timeChanged.connect(self._updateActualTime)
        self._checkActualTime: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Include")
        self._checkActualTime.toggled.connect(self._toggleActualTime)

        self._endTimeEdit: QtWidgets.QTimeEdit = QtWidgets.QTimeEdit()
        self._endTimeEdit.timeChanged.connect(self._updateEndTime)
        self._checkEndTime: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Include")
        self._checkEndTime.toggled.connect(self._toggleEndTime)

        defaultTime: QtCore.QTime = QtCore.QTime()
        defaultTime.setHMS(12, 34, 0, 0)
        for timeEdit in [self._samplingTimeEdit, self._actualTimeEdit, self._endTimeEdit]:
            timeEdit.setDisplayFormat("hh:mm")
            timeEdit.setFixedWidth(self.elementWidth)
            timeEdit.setEnabled(False)
            timeEdit.setTime(defaultTime)

        layoutDateTimeEdits: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        layoutDateTimeEdits.addWidget(QtWidgets.QLabel("Sampling End Date:"), 0, 0)
        layoutDateTimeEdits.addWidget(self._checkSampleEndDate, 0, 1)
        layoutDateTimeEdits.addWidget(self._sampleEndDateEdit, 0, 2)

        layoutDateTimeEdits.addWidget(QtWidgets.QLabel("Sampling Time/Start (UTC):"), 1, 0)
        layoutDateTimeEdits.addWidget(self._checkSamplingTime, 1, 1)
        layoutDateTimeEdits.addWidget(self._samplingTimeEdit, 1, 2)

        layoutDateTimeEdits.addWidget(QtWidgets.QLabel("Actual Time of Sampling (UTC):"), 2, 0)
        layoutDateTimeEdits.addWidget(self._checkActualTime, 2, 1)
        layoutDateTimeEdits.addWidget(self._actualTimeEdit, 2, 2)

        layoutDateTimeEdits.addWidget(QtWidgets.QLabel("Sampling End Time (UTC):"), 3, 0)
        layoutDateTimeEdits.addWidget(self._checkEndTime, 3, 1)
        layoutDateTimeEdits.addWidget(self._endTimeEdit, 3, 2)

        layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        layout.addRow(getIsMandatoryLabel())
        layout.addRow("Sampling Date*:", self._sampleDateEdit)
        layout.addRow(getIsOptionalLabel())
        optionalGroup: QtWidgets.QGroupBox = QtWidgets.QGroupBox()
        optionalGroup.setStyleSheet("QGroupBox {border: 0 px}")
        optionalLayout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        optionalLayout.addLayout(layoutDateTimeEdits)
        optionalLayout.addStretch()
        optionalGroup.setLayout(optionalLayout)
        layout.addRow(optionalGroup)

    @QtCore.pyqtSlot()
    def _updateSamplingDate(self) -> None:
        date: QtCore.QDate = self._sampleDateEdit.date()
        dateCode: DomeCode = DomeCode(QDate2String(date), "Sampling Date")
        self._tableItem.setSamplingDate(dateCode)

    @QtCore.pyqtSlot()
    def _updateSamplingEndDate(self) -> None:
        if self._checkSampleEndDate.isChecked():
            date: QtCore.QDate = self._sampleEndDateEdit.date()
            dateCode: DomeCode = DomeCode(QDate2String(date), "Sampling End Date")
            self._tableItem.setSamplingEndDate(dateCode)
        else:
            self._tableItem.setSamplingEndDate(None)

    @QtCore.pyqtSlot(bool)
    def _toggleSampleEndDate(self, checked: bool) -> None:
        self._sampleEndDateEdit.setEnabled(checked)
        self._updateSamplingEndDate()
    
    @QtCore.pyqtSlot()
    def _updateSamplingTime(self) -> None:
        if self._checkSamplingTime.isChecked():
            timeStr: str = QTime2String(self._samplingTimeEdit.time())
            timeCode: DomeCode = DomeCode(timeStr, "Sampling Time")
            self._tableItem.setSamplingTime(timeCode)
        else:
            self._tableItem.setSamplingTime(None)
    
    @QtCore.pyqtSlot(bool)
    def _toggleSamplingTime(self, checked: bool) -> None:
        self._samplingTimeEdit.setEnabled(checked)
        self._updateSamplingTime()

    @QtCore.pyqtSlot()
    def _updateActualTime(self) -> None:
        if self._checkActualTime.isChecked():
            timeStr: str = QTime2String(self._actualTimeEdit.time())
            timeCode: DomeCode = DomeCode(timeStr, "Actual Sampling Time")
            self._tableItem.setActualTime(timeCode)
        else:
            self._tableItem.setActualTime(None)

    @QtCore.pyqtSlot(bool)
    def _toggleActualTime(self, checked: bool) -> None:
        self._actualTimeEdit.setEnabled(checked)
        self._updateActualTime()

    @QtCore.pyqtSlot()
    def _updateEndTime(self) -> None:
        if self._checkEndTime.isChecked():
            timeStr: str = QTime2String(self._endTimeEdit.time())
            timeCode: DomeCode = DomeCode(timeStr, "Sampling End Time")
            self._tableItem.setEndTime(timeCode)
        else:
            self._tableItem.setEndTime(None)

    @QtCore.pyqtSlot(bool)
    def _toggleEndTime(self, checked: bool) -> None:
        self._endTimeEdit.setEnabled(checked)
        self._updateEndTime()
