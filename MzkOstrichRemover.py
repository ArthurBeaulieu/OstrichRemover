#!/usr/bin/env python3
# TODO utiliser moins de variable globale, mais faire des objets qui permettent au classe de communiquer
# faire des enum pour logger dans un dict facilement els erreur var.ENUM -> la liste des erreur


import os
import sys
import json


from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from models.track import Track
from models.folderInfo import FolderInfo
from utils.uiBuilder import printCredentials, printHelp, printRootFolderInfo, printTrackErrorInfo


##  --------  Globals  --------  ##


global scriptVersion
scriptVersion = '0.7'

global verbose
global oprhans
global debug
verbose = False
orphans = False
debug = False

global fileCounter
global errorCounter
global orphanCounter
fileCounter = 0
errorCounter = 0
orphanCounter = 0


##  --------  Main function  --------  ##


# Script main frame
def main():
    global verbose
    global orphans
    global debug
    printCredentials(scriptVersion)
    if len(sys.argv) == 2:
        scriptOptions = list(sys.argv[1])
        if '-' in scriptOptions and 'h' in scriptOptions: # Usr want to display the comand usage
            printHelp()
        else:
            crawlFolders(os.path.normpath(sys.argv[1]), computeRootFolderInfo(os.path.normpath(sys.argv[1])))
    elif len(sys.argv) == 3: # Two arguments
        scriptOptions = list(sys.argv[1])
        if 'v' in scriptOptions:
            verbose = True
        if 'o' in scriptOptions:
            orphans = True
        if 'd' in scriptOptions:
            debug = True
        crawlFolders(os.path.normpath(sys.argv[2]), computeRootFolderInfo(os.path.normpath(sys.argv[2])))
    else:
        print('No argument provided')


##  --------  Folder navigation function  --------  ##


# TODO : mettre dans fileUtils
# Will crawl the folder path given as an argument, and all its sub-directories
def crawlFolders(folder, folderInfo):
    global fileCounter
    step = 10
    percentage = step
    previousLetter = '1'
    print('  Folder crawling')
    print('> Crawling files in folder {} and all its sub-directories'.format(folder))
    print('> Folder analysis in progress...\n')
    rootPathLength = len(folder.split(os.sep))
    for root, directories, files in sorted(os.walk(folder)): # Sort directories so they are handled in the alphabetical order
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        path = root.split(os.sep) # Split root into an array of folders
        preservedPath = list(path) # Mutagen needs an preserved path when using ID3() or FLAC()
        for x in range(rootPathLength - 1): # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
            path.pop(0)
        if len(path) == 2 and path[1] != '' and verbose == True: # Artists release name -> Add in UI
            print('+ {}'.format(path[1]))
        elif len(path) == 3 and path[2] != '' and verbose == True: # Album title -> Add in UI
            print('| + {}'.format(path[2]))
        for fileName in files:
            testFile(fileName, preservedPath)
            fileCounter += 1
        # Display a progress every step % when not verbose
        if verbose == False and (fileCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter) > percentage and percentage < 100:
            purity = round(100 - round((errorCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2), 2)
            print('> Crawling completion : {:02d} % -- from {} to {} -- {} errors on {} tracks (purity : {} %)'.format(percentage - round(step / 2), previousLetter, path[1][0], errorCounter, (folderInfo.flacCounter + folderInfo.mp3Counter), purity))
            if orphans == True:
                orphanPercentage = round((orphanCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2)
                print('  including {} orphans ({} %)'.format(orphanCounter, orphanPercentage))
            percentage += step;
            previousLetter = path[1][0] # Path 1 is the Artists name
    purity = round(100 - round((errorCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2), 2)
    print('\n> Folder analysis done!')
    print('> {} errors on {} tracks (purity : {} %)'.format(errorCounter, (folderInfo.flacCounter + folderInfo.mp3Counter), purity))
    if orphans == True:
        orphanPercentage = round((orphanCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2)
        print('  including {} orphans ({} %) -- Orphans are files that aren\'t placed in an album folder (matching the track album tag)'.format(orphanCounter, orphanPercentage))


##  --------  File tests function  --------  ##

# TODO : Metttre dans fileUtils
# Manages the MP3 files to test in the pipeline
def testFile(fileName, path):
    filePath = audioTag = ''
    for folder in path: # Build the file path by concatenating folder in the file path
        filePath += '{}/'.format(folder)
    filePath += fileName # Append the filename at the end of the newly created path
    if fileName[-3:] == 'mp3' or fileName[-3:] == 'MP3': # Send the file path to the mutagen ID3 to get its tags and create the associated Track object
        track = Track('MP3', path, fileName, ID3(filePath))
    elif fileName[-4:] == 'flac' or fileName[-4:] == 'FLAC':
        track = Track('FLAC', path, fileName, FLAC(filePath))
    else:
        return
    testTrackObject(track, path) # Actual Track test


# TODO : mettre la fonction dans track
# Tests a Track object to check if it is matching the naming convention
def testTrackObject(track, path):
    global errorCounter
    global orphanCounter
    if len(track.fileNameList) < 6: # TypeError : Invalid file name (doesn't comply with the naming convention)
        orphanCounter += 1
        if orphans == True and debug == True:
            print('| KO - Filename -> The file \'{}\' isn\'t named following the naming convention. Use MzkOstrichRemover.py --help for informations'.format(track.fileName))
        return
    if debug == True:
        print('| | + {}'.format(track.fileName))
    # Track release artists and artist folder name doesn't match
    testErrorForTopic(0, track.fileNameList[0], path[len(path) - 2], track)
    # Track year and file name year doesn't match
    testErrorForTopic(1, track.fileNameList[1], track.year, track)
    # Track year and folder name year doesn't match
    testErrorForTopic(2, track.folderNameList[0], track.year, track)
    # Track album and file name album doesn't match
    testErrorForTopic(3, track.fileNameList[2], track.albumTitle, track)
    # Track album and folder name album doesn't match
    testErrorForTopic(4, track.folderNameList[1], track.albumTitle, track)
    # Track disc+track number and file name disc+track number doesn't match
    testErrorForTopic(5, track.fileNameList[3], '{}{:02d}'.format(track.discNumber, int(track.trackNumber)), track)
    # Track artists and file name artists doesn't match
    testErrorForTopic(6, track.fileNameList[4], track.artists, track)
    # Track title and file name title doesn't match  (handle both MP3 and FLAC files)
    if track.fileNameList[5][-3:] == 'mp3' or track.fileNameList[5][-3:] == 'MP3':
        testErrorForTopic(7, track.fileNameList[5][:-4], track.title, track)
    elif track.fileNameList[5][-4:] == 'flac' or track.fileNameList[5][-4:] == 'FLAC':
        testErrorForTopic(7, track.fileNameList[5][:-5], track.title, track)
    #if not track.fileNameList[5][:-5].istitle():
    #    print(track.fileNameList[5][:-5])
    #    errorCounter += 1


# Tests a Track on a given topic using an error code as documented in this function
def testErrorForTopic(errorCode, string1, string2, track):
    # TODO: utiliser l'enum
    # errorCode values :
    # 0 : Track release artists and artist folder name doesn't match
    # 1 : Track year and file name year doesn't match
    # 2 : Track year and folder name year doesn't match
    # 3 : Track album and file name album doesn't match
    # 4 : Track album and folder name album doesn't match
    # 5 : Track disc+track number and file name disc+track number doesn't match
    # 6 : Track artists and file name artists doesn't match
    # 7 : Track title and file name title doesn't match
    if string1 != string2: # The track title tag doesn't match the filename track title
        if areStringsMatchingWithFoldernameRestrictions(string1, string2) == False: # Strings do not match even w/ foldername restrictions
            # There is an error for the given topics, errorCode and strings
            global errorCounter
            topic = '                  '
            if errorCode == 0:
                topic = '-- Release artists'
            elif errorCode == 1 or errorCode == 2:
                topic = '------------- Year'
            elif errorCode == 3 or errorCode == 4:
                topic = '------------ Album'
            elif errorCode == 5:
                topic = '- Disc/TrackNumber'
            elif errorCode == 6:
                topic = '---------- Artists'
                remixerName = extractRemixerNameFromTrackTitle(string2, track)
                if remixerName != 'NOT_A_REMIX' and remixerName != string2:
                    errorCounter += 1
                    if verbose == True: # Only print errors if the script is launch in verbose mode
                        printTrackErrorInfo(topic, errorCode, remixerName, string2)
                return # Track is a remix and is properly named
            elif errorCode == 7:
                topic = '------------ Title'
            errorCounter += 1
            if verbose == True: # Only print errors if the script is launch in verbose mode
                printTrackErrorInfo(topic, errorCode, string1, string2)


##  --------  Track computations function  --------  ##

# TODO : move to fileUtils
# Reads the user given folder and store a few informations about it
def computeRootFolderInfo(folder):
    folderInfo = FolderInfo()
    # Counting file, folder in the given path and computed bytes size
    localRoot = folder
    filesCounter = foldersCounter = folderSize = 0
    mp3Counter = flacCounter = jpgCounter = pngCounter = 0
    for localRoot, dirnames, filenames in os.walk(folder):
        filesCounter += len(filenames) # Increment file counter
        foldersCounter += len(dirnames) # Increment folder counter
        for f in filenames:
            if f[-4:] == '.mp3' or f[-4:] == '.MP3': # TODO store filename in List to be dumped later in output
                mp3Counter += 1
            elif f[-5:] == '.flac' or f[-5:] == '.FLAC':
                flacCounter += 1
            elif f[-4:] == '.jpg' or f[-4:] == '.JPG':
                jpgCounter += 1
            elif f[-4:] == '.png' or f[-4:] == '.PNG':
                pngCounter += 1
            fp = os.path.join(localRoot, f)
            folderSize += os.path.getsize(fp) # Increment folder size
    # Compute files percentages
    flacPercentage = mp3Percentage = jpgPercentage = pngPercentage = 0
    if (flacCounter + mp3Counter) > 0:
        flacPercentage = round((flacCounter / (flacCounter + mp3Counter) * 100), 2)
        mp3Percentage = round((mp3Counter / (flacCounter + mp3Counter) * 100), 2)
    if (jpgCounter + pngCounter) > 0:
        pngPercentage = round((pngCounter / (jpgCounter + pngCounter) * 100), 2)
        jpgPercentage = round((jpgCounter / (jpgCounter + pngCounter) * 100), 2)
    # Log those information to the console
    folderInfo.folder = folder
    folderInfo.filesCounter = filesCounter
    folderInfo.foldersCounter = foldersCounter
    folderInfo.folderSize = folderSize
    folderInfo.flacCounter = flacCounter
    folderInfo.flacPercentage = flacPercentage
    folderInfo.mp3Counter = mp3Counter
    folderInfo.mp3Percentage = mp3Percentage
    folderInfo.pngCounter = pngCounter
    folderInfo.pngPercentage = pngPercentage
    folderInfo.jpgCounter = jpgCounter
    folderInfo.jpgPercentage = jpgPercentage
    printRootFolderInfo(folderInfo)
    return folderInfo


##  --------  Utils function  --------  ##


# TODO : déplacer dans fileUtils
# Test if the character that do not match in string are forbidden on some OS. string1 is from the filename, string2 is from the tags
def areStringsMatchingWithFoldernameRestrictions(string1, string2):
    list1 = list(string1)
    list2 = list(string2)
    # TODO: Faire des fonctions pour la vérification des . et des ... et grouper les par liste
    if len(list1) != len(list2):
        if list1[0] == '.': # Check prefix dot
            return True
        if list1[0] == '.' and list1[1] == '.' and list1[2] == '.': # Check for three prefix dots
            return True
        if list1[len(list1) - 1] == '.': # Check if the trailing char isn't a dot
            return True
        if list1[len(list1) - 1] == '.' and list1[len(list1) - 2] == '.' and list1[len(list1) - 3] == '.': # Check for 3 trailing dots
            return True
        if list2[0] == '.': # Check prefix dot
            return True
        if list2[0] == '.' and list2[1] == '.' and list2[2] == '.': # Check for three prefix dots
            return True
        if list2[len(list2) - 1] == '.': # Check if the trailing char isn't a dot
            return True
        if list2[len(list2) - 1] == '.' and list2[len(list2) - 2] == '.' and list2[len(list2) - 3] == '.': # Check for 3 trailing dots
            return True
        else:
            return False
    # Checking first that the differents char are bc of an illegal symbol
    forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|']
    for x in range(0, len(list1)):
        if list1[x] != list2[x]:
            if list1[x] == '-': # Forbidden char must have been replaced with a -, return False otherwise (char are differents for no valuable reasons)
                if list2[x] not in forbiddenChars:
                    return False
            else:
                return False
    return True

# TODO : déplacer dans fileUtils
# Extract the track remix artist name from the track fileName
def extractRemixerNameFromTrackTitle(trackTitle, track):
    if track.fileName.find(' Remix)') != -1:
        return track.fileName[track.fileName.rfind('(', 0, len(track.fileName))+1:track.fileName.find(' Remix)')]
    return ''


##  --------  Script execution zone  --------  ##


# Script start point
if __name__ == '__main__':
    main()
