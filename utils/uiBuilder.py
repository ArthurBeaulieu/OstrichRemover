from utils.tools import convertBytes

# Display script credentials
def printCredentials(scriptVersion):
    print('##--------------------------------------##')
    print('##                                      ##')
    print('##  MzkOstrichRemover.py - version {}  ##'.format(scriptVersion))
    print('##                                      ##')
    print('##--------------------------------------##\n')


# Display script 'man' page
def printHelp():
    print('  Script usage')
    print('> python MzkOstrichRemover.py ./path/to/library    : Do a crawling on the given folder')
    print('> python MzkOstrichRemover.py -h                   : Displays the script help menu')


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


# Print a detailled view of a given track. Very verbose, use carefully with big libraries
def printDetailledTrack(track):
    print('ID3 Title : {}'.format(track.title))
    print('ID3 Artists : {}'.format(track.artists))
    print('ID3 Album : {}'.format(track.albumTitle))
    print('ID3 Year : {}'.format(track.year))
    print('ID3 Performers : {}'.format(track.performers))
    print('ID3 Composers : {}'.format(track.composers))
    print('ID3 Producer : {}'.format(track.producer))
    print('ID3 Track n° : {}'.format(track.trackNumber))
    print('ID3 Track total : {}'.format(track.trackTotal))
    print('ID3 Disc n° : {}'.format(track.discNumber))
    print('ID3 Disc total : {}'.format(track.discTotal))
    print('Remixer : {}'.format(track.remix))
    print('Featuring : {}'.format(track.feat))
    print('FileType : {}'.format(track.fileType))
    print('Raw FileName : {}'.format(track.fileName))
    print('FileName list : {}'.format(track.fileNameList))
    print('FolderName list: {}'.format(track.folderNameList))
    print('Path list : {}\n'.format(track.pathList))


def printStartCrawling(targetFolder):
    print('  Folder crawling')
    print('> Crawling files in folder {} and all its sub-directories'.format(targetFolder))
    print('> Folder analysis in progress...\n')


def printEndCrawling(errorCounter, totalTracks, purity):
    print('\n> Folder analysis done!')
    print('> {} errors on {} tracks (purity : {} %)'.format(errorCounter, totalTracks, purity))


def printCrawlingProgress(percentage, previousLetter, currentLetter, errorCounter, scannedTracks, purity):
    print('> Crawling completion : {:02d} % -- from {} to {} -- {} errors on {} tracks (purity : {} %)'.format(percentage, previousLetter, currentLetter, errorCounter, scannedTracks, purity))


def printOrphansProgress(orphanCounter, folderInfo):
    orphanPercentage = round((orphanCounter * 100) / (folderInfo.flacCounter + folderInfo.mp3Counter), 2)
    print('  including {} orphans ({} %) -- Orphans are files that aren\'t placed in an album folder (matching the track album tag)'.format(orphanCounter, orphanPercentage))


def printErroredTracksReport(albumTesters):
    currentArtist = ''
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        if currentArtist != albumPathList[len(albumPathList) - 2]: # Current Artist has changed : update UI w/ new parsed artist
            print('+ {}'.format(albumPathList[len(albumPathList) - 2]))
            currentArtist = albumPathList[len(albumPathList) - 2]
        print('| + {}'.format(albumPathList[len(albumPathList) - 1])) # Print current album name
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                print('| | + {}'.format(trackTester.track.fileName))
                for error in trackTester.errors:
                    _printErroredTracksReport_aux(error.value, trackTester, albumTester)


def _printErroredTracksReport_aux(errorCode, trackTester, albumTester):
    track = trackTester.track
    if errorCode == 0: # ErrorCode 00 : Filename release artists doesn't match the artist foldername
        printTrackErrorInfo(errorCode, track.fileNameList[0], trackTester.track.pathList[len(trackTester.track.pathList) - 2])
    elif errorCode == 1: # ErrorCode 01 : Filename year doesn't match the album foldername year
        printTrackErrorInfo(errorCode, track.fileNameList[1], track.folderNameList[0])
    elif errorCode == 2: # ErrorCode 02 : Filename album doesn't match the album foldername
        printTrackErrorInfo(errorCode, track.fileNameList[2], track.folderNameList[1])
    elif errorCode == 3: # ErrorCode 03 : Filename year doesn't math the track year tag
        printTrackErrorInfo(errorCode, track.fileNameList[1], track.year)
    elif errorCode == 4: # ErrorCode 04 : Foldername year doesn't math the track year tag
        printTrackErrorInfo(errorCode, track.folderNameList[0], track.year)
    elif errorCode == 5: # ErrorCode 05 : Filename album doesn't match the track album
        printTrackErrorInfo(errorCode, track.fileNameList[2], track.albumTitle)
    elif errorCode == 6: # ErrorCode 06 : Foldername album doesn't match the track album
        printTrackErrorInfo(errorCode, track.folderNameList[1], track.albumTitle)
    elif errorCode == 7: # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
        discTrackConcat = '{}{:02d}'.format(track.discNumber, int(track.trackNumber))
        printTrackErrorInfo(errorCode, track.fileNameList[3], discTrackConcat)
    elif errorCode == 8: # ErrorCode 08 : Filename artists doesn't match the track artist tag
        printTrackErrorInfo(errorCode, track.fileNameList[4].split(', '), track.artists)
    elif errorCode == 9: # ErrorCode 09 : Title remix artist doesn't match the filename artist
        printTrackErrorInfo(errorCode, track.fileNameList[4], track.remix)
    elif errorCode == 10: # ErrorCode 10 : Filename title doesn't match the track title tag
        printTrackErrorInfo(errorCode, track.fileNameList[5].rsplit('.', 1)[0], track.title)
    elif errorCode == 11: # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
        printTrackErrorInfo(errorCode, 'Here is the list of missing tags:', trackTester.missingTags)
    elif errorCode == 12: # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
        printTrackErrorInfo(errorCode, sorted(track.performers), sorted(track.composedPerformer))
    elif errorCode == 13: # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
        printTrackErrorInfo(errorCode, 'Here is the list of misordered tags:', trackTester.missorderedTag)
    elif errorCode == 14: # ErrorCode 14 : Computed album total track is not equal to the track total track tag
        printTrackErrorInfo(errorCode, track.trackTotal, trackTester.album.trackTotal)
    elif errorCode == 15: # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
        printTrackErrorInfo(errorCode, track.discTotal, trackTester.album.discTotal)
    elif errorCode == 16: # ErrorCode 16 : Computed album yeas is not equal to the track year tag
        printTrackErrorInfo(errorCode, track.year, trackTester.album.year)



# Display the error message according to the topic and error code. It will display the two !matching values
def printTrackErrorInfo(errorCode, string1, string2):
    topic = getTopicStringFromErrorCode(errorCode)
    location1 = '                    '
    location2 = '                    '
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    # ErrorCode 01 : Filename year doesn't match the album foldername year
    # ErrorCode 02 : Filename album doesn't match the album foldername
    if errorCode == 0 or errorCode == 1 or errorCode == 2:
        location1 = 'From Filename       '
        location2 = 'From Foldername     '
    # ErrorCode 03 : Filename year doesn't math the track year tag
    # ErrorCode 05 : Filename album doesn't match the track album
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    # ErrorCode 09 : Title remix artist doesn't match the filename artist
    # ErrorCode 10 : Filename title doesn't match the track title tag
    elif errorCode == 3 or errorCode == 5 or errorCode == 7 or errorCode == 8 or errorCode == 10:
        location1 = 'From Filename       '
        location2 = 'From Track Tags     '
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    # ErrorCode 06 : Foldername album doesn't match the track album
    elif errorCode == 4 or errorCode == 6:
        location1 = 'From Foldername     '
        location2 = 'From Track Tags     '
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    elif errorCode == 9:
        location1 = 'From Filename       '
        location2 = 'From Computed Remix '
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 11:
        location1 = 'Missing Tags        '
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 12:
        location1 = 'From Performer Tag  '
        location2 = 'From Artist Tag     '
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 13:
        location1 = 'Missordered Tags    '
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    # ErrorCode 16 : Computed album yeas is not equal to the track year tag
    elif errorCode == 14 or errorCode == 15 or errorCode == 16:
        location1 = 'From Track Tags     '
        location2 = 'From Album Computed '
    print('| | | {:02d} {} -> {} : \'{}\''.format(errorCode, topic, location1, string1))
    print('| | |                            {} : \'{}\''.format(location2, string2))


def getTopicStringFromErrorCode(errorCode):
    topic = '                  '
    if errorCode == 0:
        topic = '---- Release artists'
    elif errorCode == 1 or errorCode == 3 or errorCode == 4:
        topic = '--------------- Year'
    elif errorCode == 2 or errorCode == 5 or errorCode == 6:
        topic = '-------------- Album'
    elif errorCode == 7:
        topic = '--- Disc/TrackNumber'
    elif errorCode == 8 or errorCode == 9:
        topic = '------------ Artists'
    elif errorCode == 10:
        topic = '-------------- Title'
    elif errorCode == 11 or errorCode == 13:
        topic = '--------------- Tags'
    elif errorCode == 12:
        topic = '---------- Performer'
    elif errorCode == 14:
        topic = '-- Album Total Track'
    elif errorCode == 15:
        topic = '--- Album Total Disc'
    elif errorCode == 16:
        topic = '--------- Album Year'
    return topic
