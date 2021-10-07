from typing import *

import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore

from tableItems import TableItem
from tableCollection import TableCollection


class SchemeView(QtWidgets.QGraphicsView):
    """
    Parent Class for displaying the graphical table elements and connections.
    """
    def __init__(self):
        super(SchemeView, self).__init__()
        scene: QtWidgets.QGraphicsScene = QtWidgets.QGraphicsScene()
        scene.setBackgroundBrush(QtCore.Qt.GlobalColor.lightGray)
        self.setScene(scene)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self._tableCollection: TableCollection = TableCollection()
        self._guiElements: List[TableGUIElement] = []
        self._guiMargin: int = 50  # Pixel margin between ui elements
        self._addTableElements()

    def _addTableElements(self) -> None:
        """
        Adds the ui elements according the table collection.
        :return:
        """
        self._guiElements = []

        tableItems: List[TableItem] = self._tableCollection.getTableItems()
        numElements: int = len(tableItems)
        numRows: int = int(numElements**0.5)
        numCols: float = numElements / numRows
        if numCols % 2 == 0:
            numCols: int = int(numCols)
        else:
            numCols: int = int(numCols) + 1

        elementSize: QtCore.QSize = TableGUIElement.size

        for row in range(numRows):
            for col in range(numCols):
                index: int = row * numCols + col
                if index < len(tableItems):
                    uiElement: TableGUIElement = TableGUIElement(tableItems[index])
                    self._guiElements.append(uiElement)
                    self.scene().addItem(uiElement)
                    uiElement.setX(col*elementSize.width() + (col-1)*self._guiMargin)
                    uiElement.setY(row*elementSize.width() + (row-1)*self._guiMargin)


class TableGUIElement(QtWidgets.QGraphicsItem):
    """
    Parent Class for Table elements in the GUI.
    """
    size: QtCore.QSize = QtCore.QSize(100, 100)  # Size of the graphical element
    roundCornerSize: int = 10  # Pixel size of rounded corner
    colors: Dict[bool, np.ndarray] = {True: np.array([200, 80, 80]),
                                      False: np.array([80, 200, 80])}

    def __init__(self, tableItem: TableItem):
        super(TableGUIElement, self).__init__()
        self._item: TableItem = tableItem
        self._pen: QtGui.QPen = QtGui.QPen()
        self._gradient: QtGui.QLinearGradient = QtGui.QLinearGradient()
        self._font: QtGui.QFont = QtGui.QFont()
        self.setAcceptHoverEvents(True)
        self._updatePainterProperties()

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, self.size.width(), self.size.height())

    def _updatePainterProperties(self) -> None:
        self._pen.setColor(QtCore.Qt.GlobalColor.black)
        self._gradient = QtGui.QLinearGradient(0, 0, self.boundingRect().width(), 0)
        color10: np.ndarray = self.colors[self._item.correctlySet()].astype(np.uint8)
        if self.isUnderMouse():
            color10 = (color10 * 1.2).astype(np.uint8)

        color04: np.ndarray = (color10 * 0.8).astype(np.uint8)
        color00: np.ndarray = (color04 * 0.5).astype(np.uint8)
        self._gradient.setColorAt(0.0, QtGui.QColor(color00[0], color00[1], color00[2]))
        self._gradient.setColorAt(0.4, QtGui.QColor(color04[0], color04[1], color04[2]))
        self._gradient.setColorAt(1.0, QtGui.QColor(color10[0], color10[1], color10[2]))

        self._font.setBold(True)
        self._font.setPointSize(12)

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """
        Event to overload for opening property window.
        :param event:
        :return:
        """
        pass

    def hoverEnterEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent') -> None:
        self._updatePainterProperties()

    def hoverLeaveEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent') -> None:
        self._updatePainterProperties()

    def paint(self, painter: QtGui.QPainter, option, widget) -> None:
        painter.setPen(self._pen)
        painter.setBrush(self._gradient)
        painter.setFont(self._font)
        path: QtGui.QPainterPath = QtGui.QPainterPath()
        path.addRoundedRect(self.boundingRect(), self.roundCornerSize, self.roundCornerSize)

        painter.drawPath(path)
        painter.drawText(self._getTextLocation(painter), self._item.name)

    def _getTextLocation(self, painter: QtGui.QPainter) -> QtCore.QPointF:
        """
        Determines where to draw the label text so that it appears nicely centered.
        :param painter: The QPainter object
        :return: QPointF for drawing the text
        """
        fontsize: int = painter.font().pointSize()
        textSize: QtCore.QSize = painter.fontMetrics().size(fontsize, self._item.name)
        textLoc: QtCore.QPointF = QtCore.QPointF(self.size.width() / 2 - textSize.width() / 2,
                                                 self.size.height() / 2 + textSize.height() / 4)
        return textLoc
