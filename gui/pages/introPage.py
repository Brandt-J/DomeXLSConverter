from PyQt6 import QtWidgets
import os


class IntroPage(QtWidgets.QWizardPage):
    """
    First page of the wizard, showing general information
    """
    def __init__(self):
        super(IntroPage, self).__init__()
        self.setTitle("Particle Upload Wizard")
        self.setSubTitle("Please follow the instructions in this wizard to summarize and upload "
                         "particle measurement results into the database.")

        self._xlsLoaded: bool = False
        self._dbConnected: bool = False

        self._lblXLSLoaded: QtWidgets.QLabel = QtWidgets.QLabel("No File selected.")
        self._lblConnected: QtWidgets.QLabel = QtWidgets.QLabel("DB Not connected.")

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self._btnLoadXLS: QtWidgets.QPushButton = QtWidgets.QPushButton("Load Excel File")
        self._btnLoadXLS.pressed.connect(self._loadXLSFile)
        self._btnConnectDB: QtWidgets.QPushButton = QtWidgets.QPushButton("Connect to Database")
        self._btnConnectDB.pressed.connect(self._connectToDB)

        for btn in [self._btnLoadXLS, self._btnConnectDB]:
            btn.setMaximumWidth(150)

        layout.addWidget(QtWidgets.QLabel("Please load the excel file and connect to the database."))
        layout.addWidget(self._btnLoadXLS)
        layout.addWidget(self._lblXLSLoaded)
        layout.addWidget(self._btnConnectDB)
        layout.addWidget(self._lblConnected)

    def isComplete(self) -> bool:
        return self._xlsLoaded and self._dbConnected

    def _loadXLSFile(self) -> None:
        """
        Loads the excel file that is going to be used as source for the particle data.
        :return:
        """
        fname: str = self._getXLSFileName()
        if fname:
            assert os.path.exists(fname), f'The specified file {fname} was not found.'
            self._lblXLSLoaded.setText(f"Loaded file {os.path.basename(fname)}.")
            self._xlsLoaded = True
            self.completeChanged.emit()

    def _getXLSFileName(self) -> str:
        """
        Prompts for the excel file name.
        :return:
        """
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select the Excel file", filter="*xlsx *xls")
        return fname

    def _connectToDB(self) -> None:
        """
        Connects to the database for particle upload
        :return:
        """
        self._lblConnected.setText("Not connected, but button was pressed..")
        self._dbConnected = True
        self.completeChanged.emit()
