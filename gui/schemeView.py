from PyQt6 import QtWidgets, QtGui, QtCore

from tableItems import TableItem


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

        testElement: TableElement = TableElement(TableItem("TestItem", {}))
        scene.addItem(testElement)


class TableElement(QtWidgets.QGraphicsItem):
    """
    Parent Class for Table elements.
    """
    size: QtCore.QSize = QtCore.QSize(100, 200)  # Size of the graphical element
    roundCornerSize: int = 10  # Pixel size of rounded corner

    def __init__(self, tableItem: TableItem):
        super(TableElement, self).__init__()
        self._item: TableItem = tableItem
        self._pen: QtGui.QPen = QtGui.QPen()
        self._brush: QtGui.QBrush = QtGui.QBrush()
        self._configurePenAndBrush()

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, self.size.width(), self.size.height())

    def _configurePenAndBrush(self) -> None:
        self._pen.setColor(QtCore.Qt.GlobalColor.black)
        self._brush.setColor(QtCore.Qt.GlobalColor.gray)

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """
        Event to overload for opening property window.
        :param event:
        :return:
        """
        pass

    def paint(self, painter: QtGui.QPainter, option, widget) -> None:
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        path: QtGui.QPainterPath = QtGui.QPainterPath()
        path.addRoundedRect(self.boundingRect(), self.roundCornerSize, self.roundCornerSize)
        painter.drawPath(path)

        textLoc: QtCore.QPointF = QtCore.QPointF(self.size.width()/2, self.size.height()/2)
        painter.drawText(textLoc, self._item.name)
