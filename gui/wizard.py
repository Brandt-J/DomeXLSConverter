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
from gui.pages.page_6_monitoring import MonitoringPage
from gui.pages.page_7_particles import ParticlesPage
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

        self._introPage: IntroPage = IntroPage(self._tableConverter.getXLSReader())
        self.addPage(self._introPage)

        self._idPage: IDPage = IDPage(self._tableConverter.getIDTable())
        self.addPage(self._idPage)

        self._locPage: LocationPage = LocationPage(self._tableConverter.getLocationTable())
        self.addPage(self._locPage)

        self._timePage: TimePage = TimePage(self._tableConverter.getTimeTable())
        self.addPage(self._timePage)

        self._samplePage: SamplePage = SamplePage(self._tableConverter.getSampleTable())
        self.addPage(self._samplePage)

        self._analysisPage: AnalysisPage = AnalysisPage(self._tableConverter.getAnalysisTable())
        self.addPage(self._analysisPage)

        self._monitoringPage: MonitoringPage = MonitoringPage(self._tableConverter.getMonitoringTable())
        self.addPage(self._monitoringPage)

        self._particlesPage: ParticlesPage = ParticlesPage(self._tableConverter.getParticleColumnAssignmentsTable(),
                                                           self._tableConverter.createFinalDataFrame,
                                                           self._tableConverter.getXLSReader())
        self._introPage.ActiveSheetSet.connect(self._particlesPage.setupToAvailableColumns)
        self.addPage(self._particlesPage)
