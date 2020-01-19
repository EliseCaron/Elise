from PyQt5 import QtWidgets, QtCore

import partition
import simulation
import mainview

NOTES_FILE = "test_partition.txt"
if __name__ == "__main__":
    
    #notes = partition.from_file(NOTES_FILE)
    notes = []
    sim = simulation.Simulation(notes)

    app = QtWidgets.QApplication([])

    seq = mainview.MainView(sim, notes)

    app.exec_()
