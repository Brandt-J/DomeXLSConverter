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
from typing import List

from PyQt6 import QtWidgets, QtCore

from gui.pages.page_0_intro import IntroPage
from gui.pages.page_1_id import IDPage
from gui.pages.page_2_location import LocationPage
from gui.pages.page_3_time import TimePage
from gui.pages.page_4_sample import SamplePage
from gui.pages.page_5_analysis import AnalysisPage
from gui.pages.page_6_particles import ParticlesPage
from tableConverter import TableConverter


class ParticleUploadWizard(QtWidgets.QWizard):
    """
    Main Window Class for guiding the user through the upload process.
    """
    def __init__(self):
        super(ParticleUploadWizard, self).__init__()
        self.setWindowTitle("Particle Upload Wizard")
        self.setFixedSize(QtCore.QSize(500, 600))
        self.setWizardStyle(QtWidgets.QWizard.WizardStyle.ModernStyle)
        self._tableConverter: TableConverter = TableConverter()

        introPage: IntroPage = IntroPage(self._tableConverter.getXLSReader())
        introPage.ActiveSheetSet.connect(self._setupParticleColumnAssignmentsPage)
        self.addPage(introPage)
        # self.addPage(IDPage(self._tableConverter.getIDTable()))
        # self.addPage(LocationPage(self._tableConverter.getLocationTable()))
        # self.addPage(TimePage(self._tableConverter.getTimeTable()))
        # self.addPage(SamplePage(self._tableConverter.getSampleTable()))
        # self.addPage(AnalysisPage(self._tableConverter.getAnalaysisTable()))
        self._particlesPage: ParticlesPage = ParticlesPage(self._tableConverter.getParticleColumnAssignmentsTable())
        self.addPage(self._particlesPage)

    def _setupParticleColumnAssignmentsPage(self):
        colNames: List[str] = self._tableConverter.getXLSReader().getColumnsOfActiveSheet()
        self._particlesPage.setupToAvailableColumns(colNames)
