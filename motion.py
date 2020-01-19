"""Representation of the notes and the management of their motions"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsItemGroup, QGraphicsPathItem

import partition
import mainview

COLOR = "blue"
BRUSH = QBrush(QColor(COLOR))



class CursorMotionManager:

    def __init__(self, view):
        self.mainView = view

        self.cursor = Cursor(self.mainView.simulation)
        self.mainView.scene.addItem(self.cursor)

        self.update_cursor_item()

    def update_cursor_item(self):
        
        
        #update position of the cursor
        self.cursor.update_position()
        #self.mainView.scene.removeItem(self.cursor)
        #self.mainView.scene.addItem(self.cursor)




        
class Cursor(QGraphicsEllipseItem):

    def __init__(self, simu):
        super().__init__(None)
        #self.setZvalue(1)

        #self.motion_manager = motion_manager
        self.simulation = simu
        time = self.simulation.t

        width = 0.05
        lenght = 2*49
        self.setRect(-width, -width, width, lenght)
        tooltip = str(time)
        self.setToolTip(tooltip)
        
        
        """
        pen = QPen(QColor("blue"),1/100)
        pen.setCapStyle(Qt.SquareCap)
        self.path = QPainterPath()
        self.path.moveTo(0,0)
        self.path.lineTo(0,49)
        self.item = QGraphicsPathItem(self.path, self)
        self.item.setPen(pen)
        """
    def update_position(self):
        time = self.simulation.t
        self.setPos(0.05*time, 0)
        self.setToolTip(str(time))
        """
        pen = QPen(QColor("blue"),1/100)
        pen.setCapStyle(Qt.SquareCap)
        self.path.moveTo(time*0.5,0)
        self.path.lineTo(time*0.5,49)
        self.item = QGraphicsPathItem(self.path, self)
        self.item.setPen(pen)
        """
"""
class NoteMotionManager:

    def __init__(self, view):
        self.mainView = view
        self.notes = []
        self.update_note_item
        
class NoteItem(QGraphicsRectItem):

    def __init__(self, x, y, width, height, note_on = [0x90, 60, 112]):
        super().__init__(None)

        tooltip = "note : " + str(note_on[1]) + " with velocity : " + str(note_on[2])
        self.setRect(x, y, width, height)
        self.setToolTip(tooltip)
"""      
        
