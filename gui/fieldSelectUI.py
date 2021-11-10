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

        self._codes: List['DomeCode'] = codes
        self._maxNumToShow: int = maxNumToShow
        self._btns: List[QtWidgets.QPushButton] = []

        self._searchBar: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self._searchBar.setPlaceholderText("Type for refining selection.")
        self._searchBar.textEdited.connect(self._displayBtns)
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Please select an entry from the list.\n"
                                          "Hover mouse over description for more info."))

        if len(codes) > self._maxNumToShow:
            boldFont: QtGui.QFont = QtGui.QFont()
            boldFont.setBold(True)
            warnLbl: QtWidgets.QLabel = QtWidgets.QLabel(f"Warning, large number of items ({len(codes)}), "
                                                         f"only showing the first {self._maxNumToShow} hits. Please use searchbar for refining.")
            warnLbl.setFont(boldFont)
            layout.addWidget(warnLbl)

        layout.addWidget(self._searchBar)

        btnGroup: QtWidgets.QGroupBox = QtWidgets.QGroupBox()
        btnGroup.setFlat(True)
        self._btnLayout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        btnGroup.setLayout(self._btnLayout)
        self._displayBtns("")  # i.e., display all buttons.

        scrollArea: QtWidgets.QScrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(btnGroup)
        scrollArea.setMinimumWidth(btnGroup.sizeHint().width() + 25)  # + 25 for scrollbar
        layout.addWidget(scrollArea)
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
            pattern = pattern.lower()
            self._btnLayout.addRow(QtWidgets.QLabel("Code"), QtWidgets.QLabel("Description"))
            for code in self._codes:
                if len(self._btns) < self._maxNumToShow:
                    if code.descr.lower().find(pattern) != -1 or showAll:
                        newBtn: QtWidgets.QPushButton = self._getPushButton(code)
                        newLbl: QtWidgets.QLabel = QtWidgets.QLabel(code.descr)
                        newLbl.setToolTip(code.long_descr)
                        self._btnLayout.addRow(newBtn, newLbl)
                        self._btns.append(newBtn)

    def _clearBtnLayout(self) -> None:
        for i in reversed(range(self._btnLayout.count())):
            item = self._btnLayout.itemAt(i)
            self._btnLayout.removeWidget(item.widget())

    def _getPushButton(self, code: 'DomeCode') -> QtWidgets.QPushButton:
        newBtn: QtWidgets.QPushButton = QtWidgets.QPushButton(code.code)
        newBtn.pressed.connect(self._makeEmitLambda(code))
        return newBtn

    def _makeEmitLambda(self, code: 'DomeCode') -> Callable:
        return lambda: self._emitAndClose(code)

    def _emitAndClose(self, code: 'DomeCode') -> None:
        self.CodeSelected.emit(code)
        self.close()
