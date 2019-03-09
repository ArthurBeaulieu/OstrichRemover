# Python imports
import icu

# Project imports
from utils.tools import convertBytes


# Prints script credentials
def printCredentials(scriptVersion):
    print('##----------------------------------------##')
    print('##                                        ##')
    print('##  MzkOstrichRemover.py - version {}  ##'.format(scriptVersion))
    print('##                                        ##')
    print('##----------------------------------------##\n')


# Displays an error message when the user path is invalid
def printInvalidPath(path):
    print('  The path \'{}\' is invalid...'.format(path))
    print('  It must end with a / or an \\, depending on your system\n')
    print('> Exiting MzkOstrichRemover.py')


# Prints script 'man' page
def printHelp():
    print('  Script usage')
    print('> python MzkOstrichRemover.py ./path/to/library    : Do a crawling on the given folder')
    print('> python MzkOstrichRemover.py -h                   : Displays the script help menu')


# Prints the first message before scanning folder information
def printRetrieveFolderInfo():
    print('  Retrieving folder information...\n')


# Prints the studied folder and its informations
def printRootFolderInfo(folderInfo):
    print('  Files and folders information')
    print('> Folder name  : {}'.format(folderInfo.folder))
    print('> File count   : {}'.format(folderInfo.filesCounter))
    print('> Folder count : {}'.format(folderInfo.foldersCounter))
    print('> Folder size  : {}\n'.format(convertBytes(folderInfo.folderSize)))
    print('  Library informations')
    print('> Artists : {} file(s)\n> Albums  : {} file(s)'.format(folderInfo.artistsCounter, folderInfo.albumsCounter))
    print('> Tracks  : {} file(s)\n> Covers  : {} file(s)\n'.format(folderInfo.tracksCounter, folderInfo.coversCounter))
    print('  Audio files informations')
    print('> FLAC  : {} file(s) ({} %)\n> MP3   : {} file(s) ({} %)'.format(folderInfo.flacCounter, folderInfo.flacPercentage, folderInfo.mp3Counter, folderInfo.mp3Percentage))
    print('> Total : {} file(s)\n'.format(folderInfo.flacCounter + folderInfo.mp3Counter))
    print('  Artworks informations')
    print('> PNG   : {} file(s) ({} %)\n> JPG   : {} file(s) ({} %)'.format(folderInfo.pngCounter, folderInfo.pngPercentage, folderInfo.jpgCounter, folderInfo.jpgPercentage))
    print('> Total : {} file(s)\n'.format(folderInfo.pngCounter + folderInfo.jpgCounter))


# Prints a detailled view of a given track. Very verbose, use carefully with big libraries (unless you're ok with the shell dying in the field!)
def printDetailledTrack(track):
    print('ID3 Title : {}'.format(track.title))
    print('ID3 Artists : {}'.format(track.artists))
    print('ID3 Album : {}'.format(track.albumTitle))
    print('ID3 Year : {}'.format(track.year))
    print('ID3 Performers : {}'.format(track.performers))
    print('ID3 Composers : {}'.format(track.composers))
    print('ID3 Producer : {}'.format(track.producer))
    print('ID3 Track n° : {}'.format(track.trackNumber))
    print('ID3 Track total : {}'.format(track.totalTrack))
    print('ID3 Disc n° : {}'.format(track.discNumber))
    print('ID3 Disc total : {}'.format(track.totalDisc))
    print('Remixer : {}'.format(track.remix))
    print('Featuring : {}'.format(track.feat))
    print('FileType : {}'.format(track.fileType))
    print('Raw FileName : {}'.format(track.fileName))
    print('FileName list : {}'.format(track.fileNameList))
    print('FolderName list: {}'.format(track.folderNameList))
    print('Path list : {}\n'.format(track.pathList))


# Prints the scan begin message
def printScanStart(targetFolder, totalTracks):
    print('  Folder scan : {} track(s) to test'.format(totalTracks))
    print('> Scanning files in folder \'{}\' and all its sub-directories...'.format(targetFolder))


# Prints the scan progression
def printScanProgress(percentage, previousLetter, currentLetter, errorCounter, scannedTracks, purity):
    print('> {:02d}% -- from {} to {} -- {} errors on {} tracks (purity : {} %)'.format(percentage, previousLetter, currentLetter, errorCounter, scannedTracks, purity))


# Print the scand end message
def printScanEnd(errorCounter, totalTracks, purity):
    print('  Folder analysis done!')
    print('> {} errors on {} tracks (purity : {} %)'.format(errorCounter, totalTracks, purity))


# Print a line break in console
def printLineBreak():
    print('')


# -v, --verbose : Crawl albumTesters array and print all errors as a tree
def printErroredTracksReport(albumTesters):
    print('\n  Errors in tree:')
    currentArtist = ''
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        if currentArtist != albumPathList[len(albumPathList) - 2]: # Current Artist has changed : update UI w/ new parsed artist
            print('+ {}'.format(albumPathList[len(albumPathList) - 2]))
            currentArtist = albumPathList[len(albumPathList) - 2]
        print('| + {}'.format(albumPathList[len(albumPathList) - 1])) # Print current album name
        for error in albumTester.errors:
            print('| | + Errors that are album wide:')
            print('| | |----------------------------')
            _printErroredAlbumsReport_aux(error.value)
        trackErrorWarning = False
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                if trackErrorWarning == False:
                    trackErrorWarning = True
                    print('| | + Errors that are track wide:')
                    print('| | |----------------------------')
                print('| | + {}'.format(trackTester.track.fileName))
                for error in trackTester.errors:
                    _printErroredTracksReport_aux(error.value, trackTester, albumTester)


# Auxilliary, print an error about a given track
def _printErroredTracksReport_aux(errorCode, trackTester, albumTester):
    # For acented char sorting
    collator = icu.Collator.createInstance(icu.Locale('fr_FR.UTF-8'))
    t = trackTester.track
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    if errorCode == 0:
        printTrackErrorInfo(errorCode, t.fileNameList[0], t.pathList[len(t.pathList) - 2])
    # ErrorCode 01 : Filename year doesn't match the album foldername year
    elif errorCode == 1:
        printTrackErrorInfo(errorCode, t.fileNameList[1], t.folderNameList[0])
    # ErrorCode 02 : Filename album doesn't match the album foldername
    elif errorCode == 2:
        printTrackErrorInfo(errorCode, t.fileNameList[2], t.folderNameList[1])
    # ErrorCode 03 : Filename year doesn't math the track year tag
    elif errorCode == 3:
        printTrackErrorInfo(errorCode, t.fileNameList[1], t.year)
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    elif errorCode == 4:
        printTrackErrorInfo(errorCode, t.folderNameList[0], t.year)
    # ErrorCode 05 : Filename album doesn't match the track album
    elif errorCode == 5:
        printTrackErrorInfo(errorCode, t.fileNameList[2], t.albumTitle)
    # ErrorCode 06 : Foldername album doesn't match the track album
    elif errorCode == 6:
        printTrackErrorInfo(errorCode, t.folderNameList[1], t.albumTitle)
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    elif errorCode == 7:
        discTrackConcat = '{}{:02d}'.format(t.discNumber, int(t.trackNumber))
        printTrackErrorInfo(errorCode, t.fileNameList[3], discTrackConcat)
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    elif errorCode == 8:
        printTrackErrorInfo(errorCode, t.fileNameList[4].split(', '), t.artists)
    # ErrorCode 09 : Title remix artist doesn't match the filename artist
    elif errorCode == 9:
        printTrackErrorInfo(errorCode, t.artists, t.remix)
    # ErrorCode 10 : Filename title doesn't match the track title tag
    elif errorCode == 10:
        printTrackErrorInfo(errorCode, t.fileNameList[5].rsplit('.', 1)[0], t.title)
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 11:
        printTrackErrorInfo(errorCode, 'Here is the list of missing tags:', trackTester.missingTags)
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 12:
        printTrackErrorInfo(errorCode, sorted(t.performers, key=collator.getSortKey), sorted(t.composedPerformer, key=collator.getSortKey))
    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 13:
        printTrackErrorInfo(errorCode, 'Here is the list of misordered tags:', trackTester.missorderedTag)
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    elif errorCode == 14:
        printTrackErrorInfo(errorCode, t.totalTrack, trackTester.album.totalTrack)
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    elif errorCode == 15:
        printTrackErrorInfo(errorCode, t.totalDisc, trackTester.album.totalDisc)
    # ErrorCode 16 : Computed album yeas is not equal to the track year tag
    elif errorCode == 16:
        printTrackErrorInfo(errorCode, t.year, trackTester.album.year)
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    elif errorCode == 18:
        printTrackErrorInfo(errorCode, computeNamingConventionString(), 'AC-DC - 1978 - Powerage - 105 - AC-DC - Sin City')


# Auxilliary, print an error about a given album
def _printErroredAlbumsReport_aux(errorCode):
    # ErrorCode 17 : Year is not the same on all physical files of the album
    if errorCode == 17:
        printTrackErrorInfo(errorCode, 'All files in folder does not have the same year', 'Rename them properly to remove this error')


# Display the error message according to the topic and error code. It will display the two !matching values
def printTrackErrorInfo(errorCode, string1, string2):
    topic = getTopicStringFromErrorCode(errorCode)
    location1 = '                       '
    location2 = '                       '
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    # ErrorCode 01 : Filename year doesn't match the album foldername year
    # ErrorCode 02 : Filename album doesn't match the album foldername
    if errorCode == 0 or errorCode == 1 or errorCode == 2:
        location1 = 'From Filename          '
        location2 = 'From Foldername        '
    # ErrorCode 03 : Filename year doesn't math the track year tag
    # ErrorCode 05 : Filename album doesn't match the track album
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    # ErrorCode 10 : Filename title doesn't match the track title tag
    elif errorCode == 3 or errorCode == 5 or errorCode == 7 or errorCode == 8 or errorCode == 10:
        location1 = 'From Filename          '
        location2 = 'From Track Tags        '
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    # ErrorCode 06 : Foldername album doesn't match the track album
    elif errorCode == 4 or errorCode == 6:
        location1 = 'From Foldername        '
        location2 = 'From Track Tags        '
    # ErrorCode 09 : Title remix artist doesn't match the filename artist
    elif errorCode == 9:
        location1 = 'From Track Tag         '
        location2 = 'From Computed Remix    '
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 11:
        location1 = 'Missing Tags           '
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 12:
        location1 = 'From Performer Tag     '
        location2 = 'From Computed Performer'
    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 13:
        location1 = 'Missordered Tags       '
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    # ErrorCode 16 : Computed album yeas is not equal to the track year tag
    elif errorCode == 14 or errorCode == 15 or errorCode == 16:
        location1 = 'From Track Tags        '
        location2 = 'From Computed Album    '
    # ErrorCode 17 : Year is not the same on all physical files of the album
    elif errorCode == 17:
        location1 = 'Expected Pattern       '
        location2 = 'Example                '
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    elif errorCode == 18:
        location1 = 'Expected Pattern       '
        location2 = 'Example                '
    print('| | | {:02d} {} -> {} : \'{}\''.format(errorCode, topic, location1, string1))
    print('| | |                            {} : \'{}\''.format(location2, string2))


# Prints the error topic
def getTopicStringFromErrorCode(errorCode):
    topic = '                  '
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    if errorCode == 0:
        topic = '---- Release artists'
    # ErrorCode 01 : Filename year doesn't match the album foldername year
    # ErrorCode 03 : Filename year doesn't math the track year tag
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    elif errorCode == 1 or errorCode == 3 or errorCode == 4:
        topic = '--------------- Year'
    # ErrorCode 02 : Filename album doesn't match the album foldername
    # ErrorCode 05 : Filename album doesn't match the track album
    # ErrorCode 06 : Foldername album doesn't match the track album
    elif errorCode == 2 or errorCode == 5 or errorCode == 6:
        topic = '-------------- Album'
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    elif errorCode == 7:
        topic = '--- Disc/TrackNumber'
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    # ErrorCode 09 : Title remix artist doesn't match the filename artist
    elif errorCode == 8 or errorCode == 9:
        topic = '------------ Artists'
    # ErrorCode 10 : Filename title doesn't match the track title tag
    elif errorCode == 10:
        topic = '-------------- Title'
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 11 or errorCode == 13:
        topic = '--------------- Tags'
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 12:
        topic = '---------- Performer'
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    elif errorCode == 14:
        topic = '-- Album Total Track'
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    elif errorCode == 15:
        topic = '--- Album Total Disc'
    # ErrorCode 16 : Computed album year is not equal to the track year tag
    elif errorCode == 16:
        topic = '--------- Album Year'
    # ErrorCode 17 : Year is not the same on all physical files of the album
    elif errorCode == 17:
        topic = '--- Wrong Year Files'
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    elif errorCode == 18:
        topic = '-- Wrong File Naming'
    return topic


# Display the naming convention (see https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention)
def computeNamingConventionString():
    return '%releaseArtist% - %year% - %album% - %disc n°%%track n°% - %artist% - %title%'
