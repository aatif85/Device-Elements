
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os
import csv
import pandas as pd
import numpy as np
import re
import sys

window2 = tk.Tk()    # main Window
window2.title("Devices, Entities & Element Sets")
window2.geometry("400x300")

# this is a frame for the entries of files and options for the user to chose the devices
fdsFrame = tk.LabelFrame(window2, text="Basic Inputs", padx=5, pady=5)
fdsFrame.grid(row=0, column=0, sticky="nsew")


def location():  # Directory Location
    get = filedialog.askdirectory()
    os.chdir(get)


tk.Button(fdsFrame, text="Directory", command=location, width=10, height=1).grid(row=0, column=1, padx=10, pady=10)
tk.Label(fdsFrame, width=15, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)


ELEMENT_SET_COL = 'ElementFiles/Col_elementset.txt'  # makes element for columns
ELEMENT_SET_BEAM = 'ElementFiles/Beam_elementset.txt'  # makes element for beam
ELEMENT_SET_Truss = 'ElementFiles/Truss_elementset.txt'  # makes element for Truss
onlyColEle = 'ElementFiles/Column_elementLoad.txt'  # makes element loads for columns
onlyBeamEle = 'ElementFiles/Beam_elementLoad.txt'   # makes element loads for beam
onlySlabEle = 'ElementFiles/Slab_elementLoad.txt'   # makes element loads for slab
onlyTrussEle = 'ElementFiles/truss1_elementLoad.txt'  # makes element loads for truss
dupTrussEle = 'ElementFiles/truss_elementLoadFinal.txt'   # makes element loads for truss after removing duplicate
Final_EleSET2 = 'Final_EleSet.txt'   # makes final file containing updated files
finalTrussFile = 'ElementFiles/test.txt'


def elementLoad():
    global onlyTrussEle, dupTrussEle, ELEMENT_SET_COL, ELEMENT_SET_Truss
    lines = np.loadtxt(ELEMENT_SET_COL, comments="#", delimiter=",", unpack=False)
    a1 = np.array(lines)
    lines2 = np.genfromtxt(ELEMENT_SET_Truss, comments="#", delimiter=",", unpack=False)
    a2 = np.array(lines2)
    y = np.intersect1d(a1, a2)
    myList = [int(x) for x in y]
    dupItems = list(map(str, myList))
    print(myList)
    print(dupItems)

    def should_remove_line(loadData, stop_words):
        return re.search(r"\b{}\b".format(stop_words), loadData)

    with open(onlyTrussEle) as f, open(dupTrussEle, "w") as working:
        for line in f:
            for item in dupItems:
                if should_remove_line(line, item):
                    working.write(line)

    with open(onlyTrussEle) as source:
        lines_src = source.readlines()
    with open(dupTrussEle) as source2:
        lines_src2 = source2.readlines()

    finalFile = open(finalTrussFile, "w")
    for data in lines_src:
        if data not in lines_src2:
            finalFile.write(data)

    finalFile.close()

    eleFileList = [onlyColEle, onlyBeamEle, finalTrussFile, onlySlabEle]

    with open(Final_EleSET2, 'w') as finalFile:
        for fname in eleFileList:
            try:
                open(fname, 'r')
            except IOError:
                open(fname, 'w')
            with open(fname) as infile:
                for line in infile:
                    finalFile.write(line)


tk.Button(window2, text="Update Ele. Load", command=elementLoad, width=15, height=1).grid(row=8, column=0, padx=5, pady=5)

window2.mainloop()
