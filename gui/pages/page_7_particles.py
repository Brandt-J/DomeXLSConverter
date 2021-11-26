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
from logging import getLogger
import sys

from dataimport.domeCodes import DomeCode, getLitterProperties, getPolymerTypes, getShapeParams
from gui.fontsAndLabels import getIsMandatoryLabel, getIsOptionalLabel
from gui.fieldSelectUI import SelectorPushButton

if TYPE_CHECKING:
    from tables.table_7_particle import ParticleColumnMapping, CodeMappings
    from dataimport.readXLS import XLSReader
    import pandas as pd


testRunning: bool = "pytest" in sys.modules


class ParticlesPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the particles.
    """
    elementWidth: int = 100

    def __init__(self, tableItem: 'ParticleColumnMapping', createDFrameFunc: Callable[[], 'pd.DataFrame'],
                 excelReader: 'XLSReader'):
        super(ParticlesPage, self).__init__()
        self.setTitle("Analysis Information")
        self.setSubTitle("Please select which columns from the excel sheet to use for which database field.\n"
                         "Entries marked with * are mandatory.")

        self._tableItem: 'ParticleColumnMapping' = tableItem
        self._excelReader: XLSReader = excelReader
        self._createDFrameFunc: Callable[[], pd.DataFrame] = createDFrameFunc

        self.setButtonText(QtWidgets.QWizard.WizardButton.FinishButton,
                           "Create And Save Litter Report File")

        self._codeMapper: CodeMapper = CodeMapper()
        self._codeMapper.CodeMappingChanged.connect(lambda: self.completeChanged.emit())

        self._btnShape: Union[None, SelectorPushButton] = None
        self._btnSize: Union[None, SelectorPushButton] = None
        self._btnType: Union[None, SelectorPushButton] = None
        self._btnColor: Union[None, SelectorPushButton] = None

        self._btnMapString2Shape: QtWidgets.QPushButton = QtWidgets.QPushButton("Assign Dome Codes")
        self._btnMapString2Shape.pressed.connect(self._mapShapeCodes)
        self._btnMapString2Type: QtWidgets.QPushButton = QtWidgets.QPushButton("Assign Dome Codes")
        self._btnMapString2Type.pressed.connect(self._mapTypeCodes)
        self._btnMapString2Color: QtWidgets.QPushButton = QtWidgets.QPushButton("Assign Dome Codes")
        self._btnMapString2Color.pressed.connect(self._mapColorCodes)
        for btn in [self._btnMapString2Shape, self._btnMapString2Type, self._btnMapString2Color]:
            btn.setDisabled(True)

        self.completeChanged.connect(self._columnAssignmentChanged)

    def validatePage(self) -> bool:
        """
        Called when pressing the "Finish" Button
        :return:
        """
        success: bool = False
        saveName: str = self._getSaveFileName()
        if saveName:
            if not saveName.endswith(".xlsx"):
                saveName += ".xlsx"
            try:
                assert self.isComplete(), 'Error: The Particle Page is not yet completed.'
                dframe: 'pd.DataFrame' = self._createDFrameFunc()
                dframe.to_excel(saveName)
                success = True
            except AssertionError as e:
                errmsg: str = f"Data compilation failed with error:\n{e}"
                if not testRunning:
                    QtWidgets.QMessageBox.about(self, "Error", errmsg)
                else:
                    print(errmsg)

        if success:
            msg: str = f"Export to {saveName} completed succesfully"
            if not testRunning:
                QtWidgets.QMessageBox.about(self, "Done", msg)
            else:
                print(msg)

        return success

    def _getSaveFileName(self) -> str:
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Choose save file name", filter="*xlsx")
        return fname

    def setupToAvailableColumns(self) -> None:
        availableColumns = self._excelReader.getColumnsOfActiveSheet()
        columnNameCodes: List[DomeCode] = [DomeCode(name, "FakeCode") for name in availableColumns]

        self._btnShape = SelectorPushButton(columnNameCodes, self._tableItem.setShapeColumn, self.completeChanged,
                                            hideDescriptions=True)
        self._btnSize = SelectorPushButton(columnNameCodes, self._tableItem.setSizeColumn, self.completeChanged,
                                           hideDescriptions=True)
        self._btnType = SelectorPushButton(columnNameCodes, self._tableItem.setPolymTypeColumn, self.completeChanged,
                                           hideDescriptions=True)
        self._btnColor = SelectorPushButton(columnNameCodes, self._tableItem.setColorColumn, self.completeChanged,
                                            hideDescriptions=True)

        layout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(QtWidgets.QLabel("Assigned Column"), 0, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QtWidgets.QLabel("Code Mapping"), 0, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(getIsMandatoryLabel(), 1, 0, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Column Particle Size"), 2, 0)
        layout.addWidget(self._btnSize, 2, 1)

        layout.addWidget(getIsOptionalLabel(), 3, 0, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Column Polymer Type"), 4, 0)
        layout.addWidget(self._btnType, 4, 1)
        layout.addWidget(self._btnMapString2Type, 4, 2)

        layout.addWidget(QtWidgets.QLabel("Column Polymer Shape"), 5, 0)
        layout.addWidget(self._btnShape, 5, 1)
        layout.addWidget(self._btnMapString2Shape, 5, 2)

        layout.addWidget(QtWidgets.QLabel("Column Polymer Color"), 6, 0)
        layout.addWidget(self._btnColor, 6, 1)
        layout.addWidget(self._btnMapString2Color, 6, 2)

    def isComplete(self) -> bool:
        return self._tableItem.correctlySet()

    def _mapTypeCodes(self) -> None:
        """
        Launches the Code Mapper to map Polymer Types to Dome Codes
        :return:
        """
        polymTypeColumn: Union[None, 'DomeCode'] = self._tableItem.getPolymTypeColumn()
        assert polymTypeColumn is not None, "The Type Column was not yet defined!"
        columnName: str = polymTypeColumn.code
        availableCodes: List['DomeCode'] = getPolymerTypes()
        self._launchCodeMapper(availableCodes, columnName, self._tableItem.setTypeMapping)

    def _mapShapeCodes(self) -> None:
        """
        Launches the Code Mapper to map particle shapes to Dome Codes
        :return:
        """
        shapeColumn: Union[None, 'DomeCode'] = self._tableItem.getShapeColumn()
        assert shapeColumn is not None, "The Shape Column was not yet defined!"
        columnName: str = shapeColumn.code
        availableCodes: List['DomeCode'] = getShapeParams()
        self._launchCodeMapper(availableCodes, columnName, self._tableItem.setShapeMapping)

    def _mapColorCodes(self) -> None:
        """
        Launches the Code Mapper to map particle colors to Dome Codes
        :return:
        """
        colorColumn: Union[None, 'DomeCode'] = self._tableItem.getColorColumn()
        assert colorColumn is not None, "The Color Column was not yet defined!"
        columnName: str = colorColumn.code
        availableCodes: List['DomeCode'] = getLitterProperties()
        self._launchCodeMapper(availableCodes, columnName, self._tableItem.setColorMapping)

    def _launchCodeMapper(self, availableCodes: List['DomeCode'], columnName: str,
                          updateDictFunc: Callable[[Dict[str, 'DomeCode']], None]):
        """
        Launches (i.e., set up and show) the CodeMapper with the available Codes and the name of the column in the
        currently active excel sheet from where to display the unique entries that need to be mapped
        :param availableCodes: Available Dome Codes to map to
        :param columnName: The column in the excel file from where to retrieve the unique entries
        :param updateDictFunc: The function used to save the result dictionary mapping to
        :return:
        """
        entriesInExcel: Set[str] = self._excelReader.getUniqueColumnContentsAsString(columnName)
        if len(entriesInExcel) > 0:
            self._codeMapper.setUp(entriesInExcel, availableCodes, updateDictFunc)
            if not testRunning:
                self._codeMapper.show()
        else:
            msg: str = f"There are no string type entries in the column {columnName}. " \
                       f"Please select another one."
            if not testRunning:
                QtWidgets.QMessageBox.about(self, "Error", msg)
            getLogger("Page6_Particles").info(f"Error: {msg}")

    def _columnAssignmentChanged(self) -> None:
        """
        Called when a column assignment was changed. Enables/Disables the corresponding codeMapButtons.
        :return:
        """
        selectorBtns = [self._btnShape, self._btnColor, self._btnType]
        mapBtns = [self._btnMapString2Shape, self._btnMapString2Color, self._btnMapString2Type]

        for selBtn, mapBtn in zip(selectorBtns, mapBtns):
            mapBtn.setDisabled(selBtn.text() == selBtn.DefaultText)


class CodeMapper(QtWidgets.QWidget):
    CodeMappingChanged: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(CodeMapper, self).__init__()
        self._gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle(f"Code Mapper")

        self._codeDict: Dict[str, Union['DomeCode']] = {}
        self._setResultFunc: Optional[Callable[[Dict[str, 'DomeCode']], None]] = None
        self._lbls: List[QtWidgets.QLabel] = []
        self._btns: List[SelectorPushButton] = []
        self._btnAccept: QtWidgets.QPushButton = QtWidgets.QPushButton("Accept")
        self._btnAccept.setMaximumWidth(150)
        self._btnAccept.pressed.connect(self._applyFinalCodeMapping)

        layout.addLayout(self._gridLayout)
        layout.addWidget(self._btnAccept)

    def setUp(self, lblsFromExcel: Set[str], availableCodes: List['DomeCode'],
              setResultFunc: Callable[[Dict[str, 'DomeCode']], None]) -> None:
        """
        Sets up the dialog windot to allow mapping between specific entry sets.
        :param lblsFromExcel: The available (unique) labels from the Excel file
        :param availableCodes: The available Dome codes to map to
        :param setResultFunc: The function to call when pressing the "Accept" button.
        :return:
        """
        self._clearWidgetsAndLayout()
        self._codeDict = {}
        self._setResultFunc = setResultFunc

        self._gridLayout.addWidget(QtWidgets.QLabel("Entry from Excel"), 0, 0)
        self._gridLayout.addWidget(QtWidgets.QLabel("DOME Code"), 0, 1)

        if len(lblsFromExcel) > 0:
            for row, entry in enumerate(lblsFromExcel, start=1):
                lbl: QtWidgets.QLabel = QtWidgets.QLabel(entry)
                btn: SelectorPushButton = SelectorPushButton(availableCodes, self._makeCodeAcceptFunc(entry))
                self._lbls.append(lbl)
                self._btns.append(btn)
                self._gridLayout.addWidget(lbl, row, 0)
                self._gridLayout.addWidget(btn, row, 1)
                self._codeDict[entry] = None

            self._gridLayout.setRowStretch(row, 1)

    def _makeCodeAcceptFunc(self, lblName: str) -> Callable[['DomeCode'], None]:
        return lambda x: self._setCodeToLbl(lblName, x)

    def _setCodeToLbl(self, lblName: str, code: 'DomeCode') -> None:
        self._codeDict[lblName] = code

    def _applyFinalCodeMapping(self) -> None:
        assert self._setResultFunc is not None
        if None not in self._codeDict.values():
            self._setResultFunc(self._codeDict)
            self.CodeMappingChanged.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.about(self, "Warning", "Some entries have not been mapped to a DOME code.\n"
                                                         "Please assign a code to each entry category and then proceed.")

    def _clearWidgetsAndLayout(self) -> None:
        for lbl in self._lbls:
            lbl.setParent(None)
        for btn in self._btns:
            btn.setParent(None)

        self._lbls = []
        self._btns = []

        for i in reversed(range(self._gridLayout.count())):
            item = self._gridLayout.itemAt(i)
            if item.widget() is None:
                self._gridLayout.removeItem(item)
            else:
                self._gridLayout.removeWidget(item.widget())
