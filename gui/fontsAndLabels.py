from PyQt6 import QtGui, QtWidgets


boldFont: QtGui.QFont = QtGui.QFont()
boldFont.setBold(True)


def getIsMandatoryLabel() -> QtWidgets.QLabel:
    lbl: QtWidgets.QLabel = QtWidgets.QLabel("\nMandatory:")
    lbl.setFont(boldFont)
    return lbl


def getIsOptionalLabel() -> QtWidgets.QLabel:
    lbl: QtWidgets.QLabel = QtWidgets.QLabel("\nOptional:")
    lbl.setFont(boldFont)
    return lbl

