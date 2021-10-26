from PyQt6 import QtWidgets, QtCore
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

    def __init__(self, codes: List['DomeCode']) -> None:
        super(CodeSelector, self).__init__()
        self.setWindowTitle("Select Entry")
        self.setModal(True)

        self._searchBar: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._searchBar.setPlaceholderText("Type for refining selection.")
        self._searchBar.textEdited.connect(self._refineOptions)
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Please select an entry from the list.\n"
                                          "Hover mouse over description for more info."))
        layout.addWidget(self._searchBar)

        btnGroup: QtWidgets.QGroupBox = QtWidgets.QGroupBox()
        btnGroup.setFlat(True)
        btnLayout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        btnLayout.addRow(QtWidgets.QLabel("Code"), QtWidgets.QLabel("Description"))
        btnGroup.setLayout(btnLayout)

        self._btns: List[QtWidgets.QPushButton] = []
        self._lables: List[QtWidgets.QLabel] = []
        for code in codes:
            newBtn: QtWidgets.QPushButton = self._getPushButton(code)
            newLbl: QtWidgets.QLabel = QtWidgets.QLabel(code.descr)
            newLbl.setToolTip(code.long_descr)

            self._btns.append(newBtn)
            self._lables.append(newLbl)
            btnLayout.addRow(newBtn, newLbl)

        scrollArea: QtWidgets.QScrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(btnGroup)
        scrollArea.setMinimumWidth(btnGroup.sizeHint().width() + 25)  # + 25 for scrollbar
        layout.addWidget(scrollArea)
        self.setLayout(layout)

    @QtCore.pyqtSlot(str)
    def _refineOptions(self, searchText: str) -> None:
        searchText = searchText.lower()
        showAll: bool = searchText == ""
        for btn, lbl in zip(self._btns, self._lables):
            textMatch: bool = lbl.text().lower().find(searchText) != -1
            btn.setVisible(showAll or textMatch)
            lbl.setVisible(showAll or textMatch)

    def _getPushButton(self, code: 'DomeCode') -> QtWidgets.QPushButton:
        newBtn: QtWidgets.QPushButton = QtWidgets.QPushButton(code.code)
        newBtn.pressed.connect(self._makeEmitLambda(code))
        return newBtn

    def _makeEmitLambda(self, code: 'DomeCode') -> Callable:
        return lambda: self._emitAndClose(code)

    def _emitAndClose(self, code: 'DomeCode') -> None:
        self.CodeSelected.emit(code)
        self.close()
