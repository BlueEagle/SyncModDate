import os
import sys
from os import listdir
from os.path import isfile, join

class Main:
    def __init__(self, folderName1, folderName2):
        folderName1files = [f for f in listdir(folderName1) if isfile(join(folderName1, f))]
        folderName2files = [f for f in listdir(folderName2) if isfile(join(folderName2, f))]

        mergeConflicts = []
        folder1noconflict = []
        folder2noconflict = []

        # Sort conflicts
        for filefrom1 in folderName1files:
            fileFoundInFolder2 = 0
            for filefrom2 in folderName2files:
                if filefrom2 == filefrom1:
                    fileFoundInFolder2 = 1
            if fileFoundInFolder2 == 1:
                print("Conflicting file: " + filefrom1)
                mergeConflicts += [filefrom1]

        # Sort no conflict for folder 1
        for fileName in folderName1files:
            fileMultiples = 0
            for item in mergeConflicts:
                if fileName == item:
                    fileMultiples = 1
            if fileMultiples == 0:
                print("Exclusive file (in \"" + folderName1 + "\"): " + fileName)
                folder1noconflict += [fileName]

        # Sort no conflict for folder 2
        for fileName in folderName2files:
            fileMultiples = 0
            for item in mergeConflicts:
                if fileName == item:
                    fileMultiples = 1
            if fileMultiples == 0:
                print("Exclusive file (in \"" + folderName2 + "\"): " + fileName)
                folder2noconflict += [fileName]

        # cure cancer && repopulate
        for fileName in mergeConflicts:
            f1time = os.stat(folderName1 + "\\" + fileName).st_mtime
            f2time = os.stat(folderName2 + "\\" + fileName).st_mtime
            if f1time == f2time:
                print("Conflict dismissed (no changes): " + fileName)
                continue
            if f1time > f2time:
                # f1 is latest
                print("Latest version for \"" + fileName + "\" found in: " + folderName1 + "; conflict resolved!")
                os.remove(folderName2 + "\\" + fileName)
                inFile = open(folderName1 + "\\" + fileName)
                f = open(folderName2 + "\\" + fileName, "w+")
                for line in inFile:
                    f.write(line)
                inFile.close()
                f.close()
            if f2time > f1time:
                # f2 is latest
                print("Latest version for \"" + fileName + "\" found in: " + folderName2 + "; conflict resolved!")
                os.remove(folderName1 + "\\" + fileName)
                inFile = open(folderName2 + "\\" + fileName)
                f = open(folderName1 + "\\" + fileName, "w+")
                for line in inFile:
                    f.write(line)
                inFile.close()
                f.close()

        # reproduce exclusives from folder 1 no conflict
        for fileName in folder1noconflict:
            inFile = open(folderName1 + "\\" + fileName)
            f = open(folderName2 + "\\" + fileName, "w+")
            for line in inFile:
                f.write(line)
            inFile.close()
            f.close()

        # reproduce exclusives from folder 2 no conflict
        for fileName in folder2noconflict:
            inFile = open(folderName2 + "\\" + fileName)
            f = open(folderName1 + "\\" + fileName, "w+")
            for line in inFile:
                f.write(line)
            inFile.close()
            f.close()



Main.__init__(Main, sys.argv[1], sys.argv[2])
