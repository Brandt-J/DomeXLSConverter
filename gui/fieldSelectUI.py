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


from PyQt6 import QtWidgets, QtCore, QtGui
from typing import *

from dataimport.domeCodes import DomeCode


class SelectorPushButton(QtWidgets.QPushButton):
    """
    Pushbutton variation, tied closely together to the Field Selector.
    When clicking, a FieldSelectorDialog is shown. After clicking an entry in there, the dialog closes and the
    button takes the clicked text element as text. It also connects to a function to retrieve the new entry.
    """
    def __init__(self, codeList: List['DomeCode'], connectedFunc: Callable[[DomeCode], None],
                 connectedSignal: Union[None, QtCore.pyqtSignal] = None) -> None:
        """
        :param codeList: List of codes to display.
        :param connectedFunc: Function to connect to the CodeSelected signal.
        """
        super(SelectorPushButton, self).__init__("Select Entry")
        self._selector: CodeSelector = CodeSelector(codeList)
        self.pressed.connect(self._selector.show)
        self._selector.CodeSelected.connect(self._setBtnText)
        self._selector.CodeSelected.connect(connectedFunc)
        if connectedSignal is not None:
            self._selector.CodeSelected.connect(lambda: connectedSignal.emit())

    @QtCore.pyqtSlot(DomeCode)
    def _setBtnText(self, code: DomeCode) -> None:
        self.setText(f"{code.code} ({code.descr})")


class CodeSelector(QtWidgets.QDialog):
    """
    Dialog field for selecting an enrty from a list of codes.
    """
    CodeSelected: QtCore.pyqtSignal = QtCore.pyqtSignal(DomeCode)  # Emitted with the code when clicking an entry

    def __init__(self, codes: List['DomeCode'], maxNumToShow: int = 500) -> None:
        super(CodeSelector, self).__init__()
        self.setWindowTitle("Select Entry")
        self.setModal(True)

        self._btnUseSelection: QtWidgets.QPushButton = QtWidgets.QPushButton("Use Multiple Code Selection")
        self._btnUseSelection.setMaximumWidth(170)
        self._btnUseSelection.released.connect(self._selectMultipleCodes)

        self._codes: List['DomeCode'] = codes
        self._maxNumToShow: int = maxNumToShow
        self._btns: List[QtWidgets.QPushButton] = []
        self._checkboxes: List[QtWidgets.QCheckBox] = []
        self._selectedCodes: Set[str] = set()

        self._searchBar: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._searchBar.setPlaceholderText("Type for refining selection.")
        self._searchBar.textEdited.connect(self._displayBtns)

        self._btnGroup: QtWidgets.QGroupBox = QtWidgets.QGroupBox()
        self._btnGroup.setStyleSheet("QGroupBox {border: 0px}")
        self._btnLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        self._btnGroup.setLayout(self._btnLayout)

        self._scrollArea: QtWidgets.QScrollArea = QtWidgets.QScrollArea()

        self._displayBtns("")  # i.e., display all buttons.
        self._scrollArea.setWidget(self._btnGroup)
        self._enableDisableSelectionButton()

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Click an entry from the list to select it individually.\n"
                                          "Check multiple checkboxes and click on 'Use Code Selection' to select multiple entries.\n"
                                          "Hover mouse over description for more info."))

        if len(codes) > self._maxNumToShow:
            boldFont: QtGui.QFont = QtGui.QFont()
            boldFont.setBold(True)
            warnLbl: QtWidgets.QLabel = QtWidgets.QLabel(f"Warning, large number of items ({len(codes)}), "
                                                         f"only showing the first {self._maxNumToShow} hits. Please use searchbar for refining.")
            warnLbl.setFont(boldFont)
            layout.addWidget(warnLbl)

        layout.addWidget(self._searchBar)
        layout.addWidget(self._scrollArea)
        layout.addWidget(self._btnUseSelection)
        self.setLayout(layout)

    @QtCore.pyqtSlot(str)
    def _displayBtns(self, pattern: str, minPatternLength: int = 3) -> None:
        """
        Creates and displays button for the codes of this instance. Only codes that have a description containing the
        given filter pattern are shown.
        All codes are displayed if the pattern is shorter
        :param pattern: The string to search for
        :param minPatternLength: Minimum length of the pattern. If the pattern is shorter, all entries are shown
        :return:
        """
        showAll: bool = len(pattern) < minPatternLength
        if len(pattern) >= minPatternLength or showAll:
            self._clearBtnLayout()
            self._btns = []
            self._checkboxes = []
            pattern = pattern.lower()
            self._btnLayout.addWidget(QtWidgets.QLabel("Select"), 0, 0)
            self._btnLayout.addWidget(QtWidgets.QLabel("Code"), 0, 1)
            self._btnLayout.addWidget(QtWidgets.QLabel("Description"), 0, 2)

            for row, code in enumerate(self._codes, start=1):
                if len(self._btns) < self._maxNumToShow:
                    if code.descr.lower().find(pattern) != -1 or showAll:
                        self._addSelectableCode(code, row)
                else:
                    break
        self._btnLayout.setRowStretch(self._btnLayout.rowCount(), 1)
        self._btnLayout.setColumnStretch(self._btnLayout.columnCount(), 1)
        self._scrollArea.verticalScrollBar().setSliderPosition(0)

    def _addSelectableCode(self, code: 'DomeCode', row: int) -> None:
        newBtn: QtWidgets.QPushButton = self._getPushButton(code)
        newLbl: QtWidgets.QLabel = QtWidgets.QLabel(code.descr)
        newLbl.setToolTip(code.long_descr)
        self._btns.append(newBtn)
        newCheckBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        newCheckBox.setChecked(code.code in self._selectedCodes)
        newCheckBox.stateChanged.connect(self._makeSelectLambda(newCheckBox, code))
        self._checkboxes.append(newCheckBox)
        self._btnLayout.addWidget(newCheckBox, row, 0)
        self._btnLayout.addWidget(newBtn, row, 1)
        self._btnLayout.addWidget(newLbl, row, 2)

    def _clearBtnLayout(self) -> None:
        for btn in self._btns:
            btn.pressed.disconnect()
        for box in self._checkboxes:
            box.stateChanged.disconnect()
        for i in reversed(range(self._btnLayout.count())):
            item = self._btnLayout.itemAt(i)
            if item.widget() is not None:
                self._btnLayout.removeWidget(item.widget())
            else:
                self._btnLayout.removeItem(item)

    def _getPushButton(self, code: 'DomeCode') -> QtWidgets.QPushButton:
        newBtn: QtWidgets.QPushButton = QtWidgets.QPushButton(code.code)
        newBtn.pressed.connect(self._makeEmitLambda(code))
        return newBtn

    def _makeEmitLambda(self, code: 'DomeCode') -> Callable:
        return lambda: self._emitAndClose(code)

    def _emitAndClose(self, code: 'DomeCode') -> None:
        self.CodeSelected.emit(code)
        self.close()

    def _makeSelectLambda(self, checkbox: QtWidgets.QCheckBox, code: 'DomeCode') -> Callable:
        return lambda: self._addRemoveFromSelection(checkbox, code)

    def _addRemoveFromSelection(self, checkbox: QtWidgets.QCheckBox, code: 'DomeCode') -> None:
        if checkbox.isChecked():
            self._selectedCodes.add(code.code)
        else:
            self._selectedCodes.remove(code.code)
        self._enableDisableSelectionButton()

    def _enableDisableSelectionButton(self) -> None:
        self._btnUseSelection.setEnabled(len(self._selectedCodes) >= 2)

    def _selectMultipleCodes(self) -> None:
        """
        Creates a combined DomeCode with multiple entries, according the checkbox selctions.
        :return:
        """
        if len(self._selectedCodes) < 2:
            QtWidgets.QMessageBox.about(self, "Info", "Less than codes selected.\n"
                                                      "To select an individual code, just click the resepctive button.")
        else:
            codeString: str = "~".join(self._selectedCodes)
            combinedCode: DomeCode = DomeCode(codeString, "combination")
            self._emitAndClose(combinedCode)
