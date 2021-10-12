from PyQt6 import QtWidgets
from typing import *
if TYPE_CHECKING:
    from tableItems import InstitutionTable


class InstitutionPage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the sample.
    """
    def __init__(self, tableItem: InstitutionTable):
        super(InstitutionPage, self).__init__()
        self.setTitle("Institution Information")
        self.setSubTitle("Please enter all required information about the institution.")

        self._tableItem: 'InstitutionTable' = tableItem
