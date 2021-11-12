from PyQt6 import QtWidgets, QtCore

from gui.pages.page_0_intro import IntroPage
from gui.pages.page_1_id import IDPage
from gui.pages.page_2_location import LocationPage
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

        self.addPage(IntroPage(self._tableConverter.getXLSReader()))
        self.addPage(IDPage(self._tableConverter.getIDTable()))
        self.addPage(LocationPage(self._tableConverter.getLocationTable()))
