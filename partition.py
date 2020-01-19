"""notes sample description.

This module allows to load a partition file
and to access all its information."""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPen, QBrush, QColor

BPM = 120
STEP = 1

class Notes(QtWidgets.QGraphicsRectItem):
    """ Notes data, with the following attributes:
    - note_on : list
    - note_off : list
    - start_t : int (beginning time step)
    - end_t : int (ending time step)"""

    def __init__(self,x, y, lenght = 2, width = 1, on = [0x90, 0, 0], off = [0x80, 0, 0]):
        super().__init__(x, y, lenght, width)
        self.note_on = on
        self.note_off = off
        self.start_t = None
        self.end_t = None

    def addNoteItem(self, view, notes_list):
        notes_list.append(self)
        view.scene.addItem(self)

    def mousePressEvent(self, event):
        event.accept()
        pass

def hms(t):
    """hms(int) return str
    return a formatted string MM:SS:DDD for the given time step"""
    s = t * STEP
    return "{:02d}:{:02d}:{:02d}".format(s // 360000, s //6000 % 60, s //100 %60)


def time_step(str_hms):
    """time_step(str) return int
    return the time step corresponding to a formatted string HH:MM:SS"""
    l = str_hms.replace(':', ' ').split() + [0, 0, 0]
    return (int(l[0]) * 360000 + int(l[1]) * 6000 + int(l[2]) * 100) // STEP


def from_file(filename):
    file  = open(filename)
    notes = []
    for line in file:
        words = line.strip().split()
        try:
            note_on = words[:3]
            note_off = [0x80, words[1], 0]
            note = Notes(note_on, note_off)
            note.start_t = int(words[3]) // STEP
            note.end_t = int(words[4]) // STEP
            notes.append(note)
        except Exception as error:
            print(type(error), error, line)
    file.close()
    return notes

def select(notes, t):
    """select(notes list, int) return notes list
    return the list of notes that are playing at time step t"""
    return [n for n in notes if n.start_t <= t < n.end_t]


