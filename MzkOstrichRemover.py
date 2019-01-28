#!/usr/bin/env python3


import os
import sys
import json
from mutagen.flac import FLAC
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3, BitrateMode


##  --------  Globals  --------  ##


global scriptVersion
global verbose
global oprhans
global fileCounter
global errorCounter
global orphanCounter
scriptVersion = '0.5'
verbose = False
orphans = False
fileCounter = 0
errorCounter = 0
orphanCounter = 0


##  --------  Internal class  --------  ##


# A Track container class
class Track:
    def __init__(self):
        self.title = ''
        self.artists = ''
        self.albumTitle = ''
        self.year = ''
        self.performers = ''
        self.composers = ''
        self.trackNumber = ''
        self.trackTotal = ''
        self.discNumber = ''
        self.discTotal = ''
        self.fileNameList = []
        self.folderNameList = []
        self.fileName = ''


# The target folder info class
class FolderInfo:
    def __init__(self):
        self.folder = ''
        self.filesCounter = ''
        self.foldersCounter = ''
        self.folderSize = ''
        self.flacCounter = ''
        self.flacPercentage = ''
        self.mp3Counter = ''
        self.mp3Percentage = ''
        self.pngCounter = ''
        self.pngPercentage = ''
        self.jpgCounter = ''
        self.jpgPercentage = ''


##  --------  Main function  --------  ##


# Script main frame
def main():
    global verbose
    userPath = ''
    folderInfo = ''
    printCredentials()
    if len(sys.argv) == 2:
        # Usr want to display the comand usage
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            printHelp()
        else:
            userPath = sys.argv[1]
            if userPath.endswith('/'):
                userPath = userPath[:-1]
            folderInfo = computeRootFolderInfo(userPath)
            crawlFolders(userPath, folderInfo)
    elif len(sys.argv) == 3: # Two arguments
        if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
            verbose = True
            userPath = sys.argv[2]
            if userPath.endswith('/'):
                userPath = userPath[:-1]
        folderInfo = computeRootFolderInfo(userPath)
        crawlFolders(userPath, folderInfo)
    else:
        print('No argument provided')


##  --------  Folder navigation function  --------  ##


# Will crawl the folder path given as an argument, and all its sub-directories
def crawlFolders(folder, folderInfo):
    global fileCounter
    step = 10
    percentage = step
    previousLetter = 'A'
    print('  Folder crawling')
    print('> Crawling files in folder {} and all its sub-directories'.format(folder))
    print('> Folder analysis in progress...\n')
    rootPathLength = len(folder.split(os.sep))
    for root, directories, files in sorted(os.walk(folder)): # Sort directories so they are handled in the alphabetical order
        path = root.split(os.sep)
        for x in range(rootPathLength - 1):
            path.pop(0)
        if len(path) == 2 and path[1] != '' and verbose == True: # Artists release name
            print('+ {}'.format(path[1]))
        elif len(path) == 3 and path[2] != '' and verbose == True: # Album title
            print('| + {}'.format(path[2]))
        for fileName in files:
            if fileName[-3:] == 'mp3':
                testMp3(fileName, path)
            elif fileName[-4:] == 'flac':
                testFlac(fileName, path)
            fileCounter += 1
        # Display a progress every 5% when not verbose
        if verbose == False and (fileCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter) > percentage and percentage < 100:
            purity = round(100 - round((errorCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2), 2)
            orphanPercentage =  round((orphanCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2)
            print('> Crawling completion : {:02d} % -- from {} to {} -- {} errors on {} tracks (purity : {} %)'.format(percentage - round(step / 2), previousLetter, path[1][0], errorCounter, (folderInfo.flacCounter + folderInfo.mp3Counter), purity))
            print('  including {} orphans ({} %)'.format(orphanCounter, orphanPercentage))
            percentage += step;
            previousLetter = path[1][0]
    purity = round(100 - round((errorCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2), 2)
    orphanPercentage =  round((orphanCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2)
    print('\n> Folder analysis done!')
    print('> {} errors on {} tracks (purity : {} %)'.format(errorCounter, (folderInfo.flacCounter + folderInfo.mp3Counter), purity))
    print('  including {} orphans ({} %) -- Orphans are files that aren\'t placed in an album folder (matching the track album tag)'.format(orphanCounter, orphanPercentage))


##  --------  File tests function  --------  ##


# Manages the MP3 files to test in the pipeline
def testMp3(fileName, path):
    filePath = ''
    for folder in path: # Build the file path by concatenating folder in the file path
        filePath += '{}/'.format(folder)
    filePath += fileName # Append the filename at the end of the newly created path
    audioTag = ID3(filePath) # Send the file path to the mutagen ID3 to get its tags
    track = computeTrackFromMp3(audioTag) # Create the associated Track object
    track.fileName = fileName
    track.fileNameList = computeFileNameList(fileName) # Computes its fileNameList
    track.folderNameList = computeFolderNameList(path) # Computes its folderNameList
    testTrackObject(track, path) # Actual Track test


# Manages the FLAC files to test in the pipeline
def testFlac(fileName, path):
    filePath = ''
    for folder in path: # Build the file path by concatenating folder in the file path
        filePath += '{}/'.format(folder)
    filePath += fileName # Append the filename at the end of the newly created path
    audioTag = FLAC(filePath) # Send the file path to the mutagen ID3 to get its tags
    track = computeTrackFromFlac(audioTag) # Create the associated Track object
    track.fileName = fileName
    track.fileNameList = computeFileNameList(fileName) # Computes its fileNameList
    track.folderNameList = computeFolderNameList(path) # Computes its folderNameList
    testTrackObject(track, path) # Actual Track test


# Tests a Track object to check if it is matching the naming convention
def testTrackObject(track, path):
    global errorCounter
    global orphanCounter
    if len(track.fileNameList) < 6: # TypeError : Invalid file name (doesn't comply with the naming convention)
        orphanCounter += 1
        if orphans == True:
            print('| KO - Filename -> The file \'{}\' isn\'t named following the naming convention. Use MzkOstrichRemover.py --help for informations'.format(track.fileName))
        return
    #if verbose == True:
        #print('| | + {}'.format(track.fileName))
    # The track release artists in filename isn't matching the folder in which it sits
    if track.fileNameList[0] != path[len(path) - 2]:
        errorCounter += 1
        if verbose == True:
            print('| | | KO -- Release artists -> Filename release artists   : \'{}\''.format(track.fileNameList[0]))
            print('| | |                          Foldername release artists : \'{}\''.format(path[len(path) - 2]))
    if track.fileNameList[1] != track.year: # The track year tag doesn't match the filename year
        errorCounter += 1
        if verbose == True:
            print('| | | KO ------------- Year -> Filename year              : \'{}\''.format(track.fileNameList[1]))
            print('| | |                          Track year tag             : \'{}\''.format(track.year))
    if track.folderNameList[0] != track.year: # The track year tag doesn't match the foldername year
        errorCounter += 1
        if verbose == True:
            print('| | | KO ------------- Year -> Foldername year            : \'{}\''.format(track.folderNameList[0]))
            print('| | |                          Track year tag             : \'{}\''.format(track.year))
    if track.fileNameList[2] != track.albumTitle: # The album title tag doesn't match the filename album title
        if areStringsMatchingWithFoldernameRestrictions(track.fileNameList[2], track.albumTitle) == False: # Strings do not match even w/ foldername restrictions
            errorCounter += 1
            if verbose == True:
                print('| | | KO ------------ Album -> Filename album title       : \'{}\''.format(track.fileNameList[2]))
                print('| | |                          Track album title tag      : \'{}\''.format(track.albumTitle))
    if track.folderNameList[1] != track.albumTitle: # The album title tag doesn't match the foldername album title
        if areStringsMatchingWithFoldernameRestrictions(track.folderNameList[1], track.albumTitle) == False: # Strings do not match even w/ foldername restrictions
            errorCounter += 1
            if verbose == True:
                print('| | | KO ------------ Album -> Foldername album title     : \'{}\''.format(track.folderNameList[1]))
                print('| | |                          Track album title tag      : \'{}\''.format(track.albumTitle))
    if track.fileNameList[3] != '{}{:02d}'.format(track.discNumber, int(track.trackNumber)): # The Disc/TrackNumber tag doesn't match the filename Disc/TrackNumber
        errorCounter += 1
        if verbose == True:
            print('| | | KO - Disc/TrackNumber -> Filename Disc/Track        : \'{}\''.format(track.fileNameList[3]))
            print('| | |                          Track Disc/Track tag       : \'{}{:02d}\''.format(track.discNumber, int(track.trackNumber)))
    if track.fileNameList[4] != track.artists: # The artist tag doesn't match the filename artist
        if areStringsMatchingWithFoldernameRestrictions(track.fileNameList[4], track.artists) == False: # Strings do not match even w/ foldername restrictions
            errorCounter += 1
            if verbose == True:
                print('| | | KO ---------- Artists -> Filename artists           : \'{}\''.format(track.fileNameList[4]))
                print('| | |                          Track artists tag          : \'{}\''.format(track.artists))
    if track.fileNameList[5][:-4] == '.mp3' or track.fileNameList[5][:-4] == '.MP3':
        if track.fileNameList[5][:-4] != track.title: # The track title tag doesn't match the filename track title
            if areStringsMatchingWithFoldernameRestrictions(track.fileNameList[5][:-4], track.title) == False: # Strings do not match even w/ foldername restrictions
                errorCounter += 1
                if verbose == True:
                    print('| | | KO ------------ Title -> Filename title             : \'{}\''.format(track.fileNameList[5][:-4]))
                    print('| | |                          Track title tag            : \'{}\''.format(track.title))
    elif track.fileNameList[5][:-5] == '.flac' or track.fileNameList[5][:-5] == '.FLAC':
        if track.fileNameList[5][:-5] != track.title: # The track title tag doesn't match the filename track title
            if areStringsMatchingWithFoldernameRestrictions(track.fileNameList[5][:-5], track.title) == False: # Strings do not match even w/ foldername restrictions
                errorCounter += 1
                if verbose == True:
                    print('| | | KO ------------ Title -> Filename title             : \'{}\''.format(track.fileNameList[5][:-5]))
                    print('| | |                          Track title tag            : \'{}\''.format(track.title))


##  --------  Track computations function  --------  ##


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


# Read the mp3 track ID3 tags and extract all interresting values into a Track object
def computeTrackFromMp3(audioTag):
    track = Track()
    if 'TIT2' in audioTag and audioTag['TIT2'].text[0] != '':
        track.title = audioTag['TIT2'].text[0].rstrip()
    if 'TPE1' in audioTag:
        track.artists = audioTag['TPE1'].text[0]
    if 'TALB' in audioTag:
        track.albumTitle = audioTag['TALB'].text[0].rstrip()
    if 'TDRC' in audioTag and audioTag['TDRC'].text[0].get_text() != '':
        track.year = audioTag['TDRC'].text[0].get_text()[:4].rstrip()
    if 'TCOM' in audioTag and audioTag['TCOM'].text[0] != '':
        track.composers = audioTag['TCOM'].text[0]
    if 'TOPE' in audioTag and audioTag['TOPE'].text[0] != '':
        track.performers = audioTag['TOPE'].text[0].rstrip()
    if 'TRCK' in audioTag and audioTag['TRCK'].text[0] != '':
        if '/' in audioTag['TRCK'].text[0]:
            tags = audioTag['TRCK'].text[0].rstrip().split('/')
            track.trackNumber = tags[0]
            track.trackTotal = tags[1]
        else:
            track.trackNumber = audioTag['TRCK'].text[0].rstrip()
    if 'TPOS' in audioTag and audioTag['TPOS'].text[0] != '':
        tags = audioTag['TPOS'].text[0].rstrip().split('/')
        track.discNumber = tags[0]
        if len(tags) > 1:
            track.discTotal = tags[1]
        else:
            track.discTotal = -1
    return track


# Read the flac track Vorbis tags and extract all interresting values into a Track object
def computeTrackFromFlac(audioTag):
    track = Track()
    if 'TITLE' in audioTag:
        track.title = audioTag['TITLE'][0]
    if 'DATE' in audioTag:
        track.year = audioTag['DATE'][0]
    if 'TRACKNUMBER' in audioTag:
        track.trackNumber = audioTag['TRACKNUMBER'][0]
    if 'DISCNUMBER' in audioTag:
        track.discNumber = audioTag['DISCNUMBER'][0]
    if 'TOTALDISC' in audioTag:
        track.totalDisc = audioTag['TOTALDISC'][0]
    if 'TOTALTRACK' in audioTag:
        track.totalTrack = audioTag['TOTALTRACK'][0]
    if 'COMPOSER' in audioTag:
        track.composers = audioTag['COMPOSER'][0]
    if 'PERFORMER' in audioTag:
        track.performers = audioTag['PERFORMER'][0]
    if 'ARTIST' in audioTag:
        track.artists = audioTag['ARTIST'][0]
    if 'ALBUM' in audioTag:
        track.albumTitle = audioTag['ALBUM'][0]
    return track


# Splits the filename into its components (%releaseArtists% - %year% - %albumTitle% - %discNumber%%trackNumber% - %artists% - %title%)
def computeFileNameList(fileName):
    # We split the filename into its differents parts
    fileNameList = fileName.split(' - ')
    # Here we handle all specific cases (whene ' - ' is not a separator)
    if len(fileNameList) > 6:
        if fileNameList[3] == 'Single': # When album is a single, we must re-join the album name and the 'Single' suffix
            fileNameList[2:4] = [' - '.join(fileNameList[2:4])] # Re-join with a ' - ' separator
    return fileNameList


# Splits the folderame into its components (%year% - %albumTitle%)
def computeFolderNameList(path):
    # We also split the folder name to make a double check for Year and Album name
    folderNameList = path[len(path) - 1].split(' - ')
    if len(folderNameList) > 2:
        if folderNameList[2] == 'Single': # When album is a single, we must re-join the album name and the 'Single' suffix
            folderNameList[1:3] = [' - '.join(folderNameList[1:3])] # Re-join with a ' - ' separator
    return folderNameList


##  --------  UI function  --------  ##


# Display script credentials
def printCredentials():
    print('##--------------------------------------##')
    print('##                                      ##')
    print('##  MzkOstrichRemover.py - version {}  ##'.format(scriptVersion))
    print('##                                      ##')
    print('##--------------------------------------##\n')


# Display script 'man' page
def printHelp():
    print('  Script usage')
    print('> python MzkOstrichRemover.py ./path/to/library    : Do a crawling on the given folder')
    print('> python MzkOstrichRemover.py -v ./path/to/library : Do a crawling on the given folder in verbose mode (--verbose)')
    print('> python MzkOstrichRemover.py -h                   : Displays the script help menu (--help)')
    print('> python MzkOstrichRemover.py -v                   : Displays the script version (--version)\n')


# Display the studied folder and its informations
def printRootFolderInfo(folderInfo):
    print('  Files and folders information')
    print('> Folder name  : {}'.format(folderInfo.folder))
    print('> File count   : {}'.format(folderInfo.filesCounter))
    print('> Folder count : {}'.format(folderInfo.foldersCounter))
    print('> Folder size  : {}\n'.format(convertBytes(folderInfo.folderSize)))
    print('  Audio files informations')
    print('> FLAC : {} file(s) ({} %)\n> MP3  : {} file(s) ({} %)\n'.format(folderInfo.flacCounter, folderInfo.flacPercentage, folderInfo.mp3Counter, folderInfo.mp3Percentage))
    print('  Artworks informations')
    print('> PNG : {} file(s) ({} %)\n> JPG : {} file(s) ({} %)\n'.format(folderInfo.pngCounter, folderInfo.pngPercentage, folderInfo.jpgCounter, folderInfo.jpgPercentage))


##  --------  Utils function  --------  ##


# Converts a given number to a properly formatted file size
def convertBytes(num):
    for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.2f %s' % (num, i)
        num /= 1024.0


# Test if the character that do not match in string are forbidden on some OS. string1 is from the filename, string2 is from the tags
def areStringsMatchingWithFoldernameRestrictions(string1, string2):
    list1 = list(string1)
    list2 = list(string2)
    if len(list1) != len(list2):
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
    for x in range(0, len(list1) - 1): # TODO handle several special char in one string
        if list1[x] != list2[x]:
            if list2[x] == '/' and list1[x] == '-':
                return True
            elif list2[x] == ':' and list1[x] == '-':
                return True
            elif list2[x] == '?' and list1[x] == '-':
                return True
            elif list2[x] == '<' and list1[x] == '-':
                return True
            elif list2[x] == '>' and list1[x] == '-':
                return True
            elif list2[x] == ';' and list1[x] == ',':
                return True
    return False


##  --------  Script execution zone  --------  ##


# Script start point
if __name__ == '__main__':
    main()
