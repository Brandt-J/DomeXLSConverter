from PyQt6 import QtWidgets, QtCore
from typing import *

from gui.pages.introPage import IntroPage
from gui.pages.institutionPage import InstitutionPage
from gui.pages.samplePage import SamplePage
from tableCollection import TableCollection


class ParticleUploadWizard(QtWidgets.QWizard):
    """
    Main Window Class for guiding the user through the upload process.
    """
    def __init__(self):
        super(ParticleUploadWizard, self).__init__()
        self.setWindowTitle("Particle Upload Wizard")
        self.setFixedSize(QtCore.QSize(500, 600))
        self._tableCollection: TableCollection = TableCollection()

        self.addPage(IntroPage())
        self.addPage(InstitutionPage(self._tableCollection.getInstitutionTable()))
        self.addPage(SamplePage())


