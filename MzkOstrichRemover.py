#!/usr/bin/env python3


import os
import sys
import json


from models.folderInfo import FolderInfo
from utils.errorEnum import ErrorEnum
from utils.uiBuilder import *
from utils.albumTester import AlbumTester
from utils.tools import computePurity


##  --------  Globals  --------  ##


global scriptVersion
scriptVersion = '0.8'


# Script main frame
def main():
    printCredentials(scriptVersion)
    if len(sys.argv) == 2:
        if '-h' in sys.argv[1]: # Usr want to display the comand usage
            printHelp()
        else:
            crawlFolders(os.path.normpath(sys.argv[1]))
    else:
        print('No argument provided')


# Will crawl the folder path given as an argument, and all its sub-directories
def crawlFolders(folder):
    folderInfo = FolderInfo(folder)
    printRootFolderInfo(folderInfo)
    printStartCrawling(folder)

    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    scannedTracks = 0
    fileCounter = 0
    errorCounter = 0
    albumTesters = []

    step = 10
    percentage = step
    previousLetter = '1' # ordered folder/file parsing begins with numbers
    rootPathLength = len(folder.split(os.sep))

    for root, directories, files in sorted(os.walk(folder)): # Sort directories so they are handled in the alphabetical order
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories

        path = root.split(os.sep) # Split root into an array of folders
        preservedPath = list(path) # Mutagen needs an preserved path when using ID3() or FLAC()

        for x in range(rootPathLength - 1): # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
            path.pop(0)

        if len(path) == 3 and path[2] != '': # Current path is for an album directory : perform tests
            albumTester = AlbumTester(files, preservedPath)
            scannedTracks += albumTester.album.trackTotal
            errorCounter += albumTester.errorCounter
            errorCounter += albumTester.tracksErrorCounter()
            albumTesters.append(albumTester)
            # Display a progress every step %
            if (scannedTracks * 100) / totalTracks > percentage and percentage < 100:
                printCrawlingProgress(percentage, previousLetter, path[1][0], errorCounter, scannedTracks, computePurity(errorCounter, scannedTracks))
                percentage += step;
                previousLetter = path[1][0] # Path 1 is the Artists name
                #printOrphansProgress(0, folderInfo)

    printErroredTracksReport(albumTesters)
    printEndCrawling(0, folderInfo.flacCounter + folderInfo.mp3Counter, computePurity(errorCounter, scannedTracks));
    printOrphansProgress(0, folderInfo)


# Script start point
if __name__ == '__main__':
    main()
