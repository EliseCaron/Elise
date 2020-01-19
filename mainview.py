"""Main view of the sequencer.

This module allows the visualization of the notes
on a scalable graphics view"""

import numpy as np
import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPen, QBrush, QColor, QCursor

import partition
import motion
import notes


WIDTH = 800
HEIGHT = 450
ANIMATION_DELAY = 20 #milliseconds

class PanZoomView(QtWidgets.QGraphicsView):
    """An interactive view that supports Pan and Zoom functions"""

    def __init__(self, scene):
        super().__init__(scene)
        # enable anti-aliasing
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # enable drag and drop of the view
        self.setDragMode(self.ScrollHandDrag)
        self.xs = []
        self.ys = []
        self.setTransformationAnchor(self.NoAnchor)
        self.hScrollBar = self.horizontalScrollBar()
        self.vScrollBar = self.verticalScrollBar() 

    def wheelEvent(self, event):
        """Overrides method in QGraphicsView in order to zoom it when mouse scroll occurs"""
        factor = math.pow(1.001, event.angleDelta().y())
        self.zoom_view(factor)
        
    
    @QtCore.pyqtSlot(int)

    
    @QtCore.pyqtSlot(int)
    
    def zoom_view(self, factor):
        """Updates the zoom factor of the view"""
##        self.setTransformationAnchor(self.AnchorUnderMouse)
##        super().scale(factor, factor)
        posVue1 = self.mapFromGlobal(QCursor.pos())
        posScene =self.mapToScene(posVue1)
        super().scale(factor, factor)
        posVue2 =self.mapFromScene(posScene)
        dxVue = posVue2.x() - posVue1.x()
        dyVue = posVue2.y() - posVue1.y()
        self.hScrollBar.setValue(self.hScrollBar.value()+dxVue)
        self.vScrollBar.setValue(self.vScrollBar.value()+dyVue)


class MainView(QtWidgets.QWidget):

    def __init__(self, simu, notes_list):
        super().__init__()
        self.simulation = simu
        self.time_increment = 1
        self.notes_list = notes_list

        #Settings
        self.setWindowTitle('Séquenceur')
        self.resize(WIDTH, HEIGHT)

        #create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = PanZoomView(self.scene)
        self.time_entry = QtWidgets.QLineEdit()
        toolbar = self.create_toolbar()
        
        self.moving_cursor = motion.CursorMotionManager(self)


        #add the sequencer elements
        self.add_sequencer_items()
        self.fit_scene_in_view()
        

        #add components to the root layout
        root_layout.addLayout(toolbar)
        root_layout.addWidget(self.view)

        #create and setup the timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.advance)
        
        #show the window
        self.show()

    def create_toolbar(self):
        toolbar = QtWidgets.QHBoxLayout()

        def add_button(text, slot):
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(slot)
            toolbar.addWidget(button)
        

        add_button('play',self.play)
        add_button('pause',self.pause)
        toolbar.addWidget(self.time_entry)
        self.time_entry.setInputMask("00:00:00")
        self.time_entry.editingFinished.connect(self.change_time)
        self.time_entry.setText(partition.hms(self.simulation.t))
        toolbar.addStretch()

        #shortcuts
        def add_shortcuts(text, slot):
            """creates an application-wide key binding"""
            shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(text), self)
            shortcut.activated.connect(slot)

        
        return toolbar
    def add_sequencer_items(self):

        seq_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(seq_group)
        Blanches = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']
        

        #Notes blanches
        pen = QPen(QtGui.QColor("white"))
        for i in range(49):
            item = QtWidgets.QGraphicsRectItem(-2*1.5, 2*i + 0.5, 2.5, 1, seq_group)
            item.setPen(pen)
            item.setToolTip(Blanches[i%7])

        #Notes noires
        pen = QPen(QtGui.QColor("black"))
        for i in range(7):
            item = QtWidgets.QGraphicsRectItem(-2*2, 2*(7*i + 1), 2.5, 0, seq_group)
            item.setPen(pen)
            item.setToolTip("Do#")
            item = QtWidgets.QGraphicsRectItem(-2*2, 2*(7*i + 2), 2.5, 0, seq_group)
            item.setPen(pen)
            item.setToolTip("Re#")
            item = QtWidgets.QGraphicsRectItem(-2*2, 2*(7*i + 4), 2.5, 0, seq_group)
            item.setPen(pen)
            item.setToolTip("Fa#")
            item = QtWidgets.QGraphicsRectItem(-2*2, 2*(7*i + 5), 2.5, 0, seq_group)
            item.setPen(pen)
            item.setToolTip("Sol#")
            item = QtWidgets.QGraphicsRectItem(-2*2, 2*(7*i + 6), 2.5, 0, seq_group)
            item.setPen(pen)
            item.setToolTip("La#")

            
        #Fin piano
        pen = QPen(QtGui.QColor("black"),1/100)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        path = QtGui.QPainterPath()
        path.moveTo(0,0)
        path.lineTo(0,49*2)
        item = QtWidgets.QGraphicsPathItem(path, seq_group)
        item.setPen(pen)

        #NoteLines
        pen = QPen(QtGui.QColor("black"),1/100)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        path = QtGui.QPainterPath()
        for i in range(49):
            path.moveTo(-4, 2*i)
            path.lineTo(0, 2*i)
            
        for i in range(7):
            path.moveTo(-4,14*i)
            path.lineTo(500, 14*i)
            
            path.moveTo(0, 14*i + 1.5)
            path.lineTo(500, 14*i + 1.5)
            
            path.moveTo(0, 14*i + 2.5)
            path.lineTo(500, 14*i + 2.5)
            
            path.moveTo(0, 14*i + 3.5)
            path.lineTo(500, 14*i + 3.5)
            
            path.moveTo(0, 14*i + 4.5)
            path.lineTo(500, 14*i + 4.5)
            
            path.moveTo(-4, 14*i + 6)
            path.lineTo(500, 14*i + 6)
            
            path.moveTo(0, 14*i + 7.5)
            path.lineTo(500, 14*i + 7.5)
            
            path.moveTo(0, 14*i + 8.5)
            path.lineTo(500, 14*i + 8.5)
            
            path.moveTo(0, 14*i + 9.5)
            path.lineTo(500, 14*i + 9.5)
            
            path.moveTo(0, 14*i + 10.5)
            path.lineTo(500, 14*i + 10.5)
            
            path.moveTo(0, 14*i + 11.5)
            path.lineTo(500, 14*i + 11.5)

            path.moveTo(0, 14*i + 12.5)
            path.lineTo(500, 14*i + 12.5)

            
        item = QtWidgets.QGraphicsPathItem(path, seq_group)
        item.setPen(pen)

    def fit_scene_in_view(self):
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def update_cursor(self):
        self.moving_cursor.update_cursor_item()
        self.time_entry.setText(partition.hms(self.simulation.t))
        
    @QtCore.pyqtSlot()
    def change_time(self):
        """slot triggered when a new time is input in the text field"""
        self.simulation.set_time(partition.time_step(self.time_entry.text()))
        self.time_entry.clearFocus()
        self.update_cursor()
        
    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out"""
        self.simulation.increment_time(self.time_increment)
        self.update_cursor()
        print("step")

    @QtCore.pyqtSlot(int)
    def set_time_increment(self, dt):
        """this slot updates the speed of the replay"""
        self.time_increment = dt
        #self.speed_slider.setValue(dt)

    @QtCore.pyqtSlot()
    def play(self):
        """this slot toggles the replay using the timer as model"""
        self.timer.start(ANIMATION_DELAY)
        print('start')

    def pause(self):
        self.timer.stop()
        print('stop')


    def mouseDoubleClickEvent(self, event):
        event.accept()
        pos1 = self.view.mapFromGlobal(QCursor.pos())
        scene_pos = self.view.mapToScene(pos1)
        #scene_pos = self.view.mapToScene(event.pos())
        self.view.xs.append(scene_pos.x())
        self.view.ys.append(scene_pos.y())
        item = NoteItem(scene_pos.x(), scene_pos.y(), self)
        item.addNoteItem(self, self.notes_list)
        print(item.x,scene_pos.x(), item.y, scene_pos.y())
        #item = self.scene.addRect(scene_pos.x(), scene_pos.y(), 2, 0)
        print(self.notes_list)


            
class NoteItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, x, y, view, lenght = 2, width = 0, on = [0x90, 0, 0], off = [0x80, 0, 0]):
        super().__init__(x, int(y), lenght, width)
        self.x = x
        self.y = y
        self.lenght = lenght
        self.width = width
        self.time_of_start(self.x)
        self.time_of_stop(self.start_t, self.lenght)
        self.note_on = on
        self.note_off = off
        #self.setPos(x, int(y))

        
        self.state_idle = 0
        self.state_dragging = 1
        self.state_resize = 2
        self.state = self.state_idle
        self.setAcceptHoverEvents(True)
##        self.notes_possibles = [i for i in range(49*2) if i%7 != 6]
        self.setMidiParam(int(self.y), 112)

    def __repr__(self):
        return "<mainview.Note {},{},{}>".format(self.start_t, self.end_t, self.note_on[1:])
        
    def setMidiParam(self, channel, velocity):
        self.note_on = [0x90, channel, velocity]
        self.note_off = [0x80, channel, 0]

    def addNoteItem(self, view, notes_list):
        if not self in notes_list:
            notes_list.append(self)
        view.scene.addItem(self)

    def addLenght(self, dx):
        self.lenght = self.lenght + dx
        self.setRect(self.x, int(self.y), self.lenght, self.width)

    def time_of_start(self, position):
        self.start_t = position/(50*0.05)

    def time_of_stop(self, start, position):
        self.end_t = self.start_t + position/(50*0.05)

    def mouseHoverEvent(self, event):
        event.accept()
        if event.pos().x() >= self.lenght-1:
            self.setCursor(QtCore.Qt.SizeHorCursor)

    def mousePressEvent(self, event):
        event.accept()
        if event.pos().x() <= self.lenght-1:
            self.state = self.state_dragging
        else:
            self.state = self.state_resize
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.state == self.state_dragging:
            event.accept()
            self.state = self.state_idle

    def mouseMoveEvent(self, event):
        event.accept()

        if self.state == self.state_dragging:
            event.accept()

            pos1 = self.view.mapFromGlobal(QCursor.pos())
            scene_pos = self.view.mapToScene(pos1)


            (x0, y0) = scene_pos.x(), scene_pos.y()

            self.setPos(x0, int(y0))
            
        elif self.state == self.state_resize:
            event.accept()
            scene_pos = self.mapToScene(event.pos())
            (x0, y0) = scene_pos.x(), scene_pos.y()

            dx = x0 - self.x
        
            self.addLenght(dx)

            

            
            

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ex = MainView()

    app.exec_()
