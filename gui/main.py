from PyQt6 import QtWidgets
import sys

from gui.wizard import ParticleUploadWizard


def main() -> None:
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    wizard: ParticleUploadWizard = ParticleUploadWizard()
    wizard.show()
    app.exec()


if __name__ == '__main__':
    main()
