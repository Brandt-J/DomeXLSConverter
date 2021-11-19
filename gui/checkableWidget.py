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
from typing import cast

from PyQt6 import QtWidgets, QtCore


class CheckableWidget(QtWidgets.QWidget):
    def __init__(self, widget: QtWidgets.QWidget):
        super(CheckableWidget, self).__init__()
        self._widget: QtWidgets.QWidget = widget
        self._widget.setDisabled(True)
        self._checkbox: QtWidgets.QCheckBox = QtWidgets.QCheckBox("Include")
        self._checkbox.toggled.connect(self._toggleWidget)

        layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._checkbox)
        layout.addWidget(self._widget)
        layout.addStretch()

    def getWidget(self) -> QtWidgets.QWidget:
        return self._widget

    def isChecked(self) -> bool:
        return self._checkbox.isChecked()

    def setChecked(self, checked: bool) -> None:
        self._checkbox.setChecked(checked)

    def setMaximumWidth(self, maxw: int) -> None:
        self._widget.setMaximumWidth(maxw)

    @QtCore.pyqtSlot(bool)
    def _toggleWidget(self, checked: bool) -> None:
        self._widget.setEnabled(checked)
        self._emitChangedSignal()

    def _emitChangedSignal(self) -> None:
        raise NotImplementedError


class CheckableDoubleSpinBox(CheckableWidget):
    Changed: QtCore.pyqtSignal = QtCore.pyqtSignal(bool, float)

    def __init__(self):
        super(CheckableDoubleSpinBox, self).__init__(QtWidgets.QDoubleSpinBox())
        self._widget: QtWidgets.QDoubleSpinBox = cast(QtWidgets.QDoubleSpinBox, self._widget)
        self._widget.valueChanged.connect(self._emitChangedSignal)

    def _emitChangedSignal(self) -> None:
        self.Changed.emit(self.isChecked(), self._widget.value())

    def setMinimum(self, value: float) -> None:
        self._widget.setMinimum(value)

    def setMaximum(self, value: float) -> None:
        self._widget.setMaximum(value)

    def setDecimals(self, value: int) -> None:
        self._widget.setDecimals(value)

    def setValue(self, value: float) -> None:
        self._widget.setValue(value)

    def getValue(self) -> float:
        return self._widget.value()

class CheckableSpinBox(CheckableWidget):
    Changed: QtCore.pyqtSignal = QtCore.pyqtSignal(bool, int)

    def __init__(self):
        super(CheckableSpinBox, self).__init__(QtWidgets.QSpinBox())
        self._widget: QtWidgets.QSpinBox = cast(QtWidgets.QSpinBox, self._widget)
        self._widget.valueChanged.connect(self._emitChangedSignal)

    def _emitChangedSignal(self) -> None:
        self.Changed.emit(self.isChecked(), self._widget.value())

    def setMinimum(self, value: int) -> None:
        self._widget.setMinimum(value)

    def setMaximum(self, value: int) -> None:
        self._widget.setMaximum(value)

    def setValue(self, value: int) -> None:
        self._widget.setValue(value)

    def getValue(self) -> float:
        return self._widget.value()
