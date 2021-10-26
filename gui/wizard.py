from PyQt6 import QtWidgets, QtCore

from gui.pages.page_0_intro import IntroPage
from gui.pages.page_1_id import IDPage
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

        self.addPage(IntroPage())
        self.addPage(IDPage(self._tableConverter.getInstitutionTable()))
