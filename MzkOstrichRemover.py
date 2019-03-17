#!/usr/bin/env python3

# Python imports
import os
import sys
import json
import argparse

# Project imports
from models.folderInfo import FolderInfo
from utils.errorEnum import ErrorEnum
from utils.albumTester import AlbumTester
from utils.tools import computePurity
from utils.reportBuilder import *
from utils.uiBuilder import *

# Globals
global scriptVersion
scriptVersion = '1.0.1'


# Script main frame
def main():
    # Init argparse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('folder', help='The input folder path to crawl (absolute or relative)')
    ap.add_argument('-d', '--dump', help='Dump errors as JSON in ./output folder', action='store_true')
    ap.add_argument('-v', '--verbose', help='Display errors as a tree after crawling', action='store_true')
    arg = ap.parse_args()
    args = vars(ap.parse_args())
    # Exec script
    printCredentials(scriptVersion)
    crawlFolders(args)


# Will crawl the folder path given in argument, and all its sub-directories
def crawlFolders(args):
    if not args['folder'].endswith('\\') and not args['folder'].endswith('/'):
        printInvalidPath(args['folder'])
        sys.exit(-1)
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Scan internals
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    rootPathLength = len(args['folder'].split(os.sep))
    scannedTracks = 0
    fileCounter = 0
    errorCounter = 0
    albumTesters = []
    # Scan progression utils
    step = 10
    percentage = step
    previousLetter = '1' # ordered folder/file parsing begins with numbers
    # Start scan
    printScanStart(args['folder'], totalTracks)
    for root, directories, files in sorted(os.walk(args['folder'])): # Sort directories so they are handled in the alphabetical order
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        path = root.split(os.sep) # Split root into an array of folders
        preservedPath = list(path) # Mutagen needs a preserved path when using ID3() or FLAC()
        for x in range(rootPathLength - 1): # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumTester = AlbumTester(files, preservedPath)
            scannedTracks += albumTester.album.totalTrack
            errorCounter += albumTester.errorCounter
            errorCounter += albumTester.tracksErrorCounter()
            albumTesters.append(albumTester)
            # Display a progress every step %
            scannedPercentage = (scannedTracks * 100) / totalTracks
            if totalTracks > 10 and scannedPercentage >= step:
                if (scannedTracks * 100) / totalTracks > percentage and percentage < 100:
                    printScanProgress(percentage, previousLetter, path[0][0], errorCounter, scannedTracks, computePurity(errorCounter, scannedTracks))
                    percentage += step;
                    previousLetter = path[0][0] # path[0] is the Artists name
    if totalTracks <= 10:
        printLineBreak()
    printScanEnd(errorCounter, totalTracks, computePurity(errorCounter, scannedTracks));
    # Compute and save JSON report
    if args['dump']:
        saveReportFile(computeReport(scriptVersion, folderInfo, albumTesters, errorCounter, computePurity(errorCounter, scannedTracks)))
    # Verbose report
    if args['verbose']:
        printErroredTracksReport(albumTesters)


# Script start point
if __name__ == '__main__':
    main()
