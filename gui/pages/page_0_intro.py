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

import os
from typing import *
from PyQt6 import QtWidgets

if TYPE_CHECKING:
    from dataimport.readXLS import XLSReader


class IntroPage(QtWidgets.QWizardPage):
    """
    First page of the wizard, showing general information
    """
    def __init__(self, xlsReader: 'XLSReader'):
        super(IntroPage, self).__init__()
        self.setTitle("Particle Upload Wizard")
        self.setSubTitle("Please follow the instructions in this wizard to summarize and upload "
                         "particle measurement results into the database.")

        self._xlsReader: 'XLSReader' = xlsReader
        self._xlsLoaded: bool = False
        self._lblXLSLoaded: QtWidgets.QLabel = QtWidgets.QLabel("No File selected.")

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self._btnLoadXLS: QtWidgets.QPushButton = QtWidgets.QPushButton("Load Excel File")
        self._btnLoadXLS.pressed.connect(self._loadXLSFile)
        self._btnLoadXLS.setMaximumWidth(150)

        layout.addWidget(QtWidgets.QLabel("Please load the excel file and connect to the database."))
        layout.addWidget(self._btnLoadXLS)
        layout.addWidget(self._lblXLSLoaded)

    def isComplete(self) -> bool:
        return self._xlsLoaded

    def _loadXLSFile(self) -> None:
        """
        Loads the excel file that is going to be used as source for the particle data.
        :return:
        """
        fname: str = self._getXLSFileName()
        if fname:
            assert os.path.exists(fname), f'The specified file {fname} was not found.'
            self._xlsReader.readXlsFile(fname)
            sheetNames: List[str] = self._xlsReader.getSheetNames()
            sheet, ok = QtWidgets.QInputDialog.getItem(self, "Choose datasheet", "Choose from the sheets", sheetNames)
            if ok and sheet:
                self._xlsReader.setActiveSheet(sheet)
                self._xlsLoaded = True
                self._lblXLSLoaded.setText(f"Loaded sheet '{sheet}' of file '{os.path.basename(fname)}'.")
                self.completeChanged.emit()

    def _getXLSFileName(self) -> str:
        """
        Prompts for the excel file name.
        :return:
        """
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select the Excel file", filter="*xlsx *xls")
        return fname
