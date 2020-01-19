"""Sequencer simulation

This module defines the interactions with the simulation"""


import partition

SHORTCUTS = """Shortcuts:
q: close window"""

class Simulation:
    """The simulation state, with the following attributes:
    - sequenceur sequencer.Sequencer
    - notes
    - t : int (current time step)"""

    def __init__(self, notes, init_time=0):
        #self.sequencer = seq
        self.notes = notes
        self.t = init_time
        self.current_notes = partition.select(self.notes, self.t)

    def set_time(self, t):
        """set_time(int): set the current time to 't'"""
        self.t = t
        self.current_notes = partition.select(self.notes, self.t)

    def increment_time(self, dt):
        """increment_time(int): increases the current time step by 'dt'
        (dt might be negative)"""
        self.set_time(self.t + dt)
