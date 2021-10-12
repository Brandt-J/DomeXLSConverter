from PyQt6 import QtWidgets


class SamplePage(QtWidgets.QWizardPage):
    """
    Wizard page for gathering information about the sample.
    """
    def __init__(self):
        super(SamplePage, self).__init__()
        self.setTitle("Sample Information")
        self.setSubTitle("Please enter all required information about the sample.")
