def buildJSONReport(albumTesters):
    jsonOutput = {}
    currentArtist = ''
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        if currentArtist != albumPathList[len(albumPathList) - 2]: # Current Artist has changed : update UI w/ new parsed artist
            jsonsOutput[currentArtist] = {}
            currentArtist = albumPathList[len(albumPathList) - 2]
        jsonsOutput[currentArtist].name = currentArtist
        jsonsOutput[currentArtist].albums = []

        for error in albumTester.errors:
            _printErroredAlbumsReport_aux(error.value)
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                for error in trackTester.errors:
                    _printErroredTracksReport_aux(error.value, trackTester, albumTester)


def _printErroredTracksReport_aux(errorCode, trackTester, albumTester):
    t = trackTester.track
    if errorCode == 0: # ErrorCode 00 : Filename release artists doesn't match the artist foldername
        printTrackErrorInfo(errorCode, t.fileNameList[0], t.pathList[len(t.pathList) - 2])
    elif errorCode == 1: # ErrorCode 01 : Filename year doesn't match the album foldername year
        printTrackErrorInfo(errorCode, t.fileNameList[1], t.folderNameList[0])
    elif errorCode == 2: # ErrorCode 02 : Filename album doesn't match the album foldername
        printTrackErrorInfo(errorCode, t.fileNameList[2], t.folderNameList[1])
    elif errorCode == 3: # ErrorCode 03 : Filename year doesn't math the track year tag
        printTrackErrorInfo(errorCode, t.fileNameList[1], t.year)
    elif errorCode == 4: # ErrorCode 04 : Foldername year doesn't math the track year tag
        printTrackErrorInfo(errorCode, t.folderNameList[0], t.year)
    elif errorCode == 5: # ErrorCode 05 : Filename album doesn't match the track album
        printTrackErrorInfo(errorCode, t.fileNameList[2], t.albumTitle)
    elif errorCode == 6: # ErrorCode 06 : Foldername album doesn't match the track album
        printTrackErrorInfo(errorCode, t.folderNameList[1], t.albumTitle)
    elif errorCode == 7: # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
        discTrackConcat = '{}{:02d}'.format(t.discNumber, int(t.trackNumber))
        printTrackErrorInfo(errorCode, t.fileNameList[3], discTrackConcat)
    elif errorCode == 8: # ErrorCode 08 : Filename artists doesn't match the track artist tag
        printTrackErrorInfo(errorCode, t.fileNameList[4].split(', '), t.artists)
    elif errorCode == 9: # ErrorCode 09 : Title remix artist doesn't match the filename artist
        printTrackErrorInfo(errorCode, t.fileNameList[4], t.remix)
    elif errorCode == 10: # ErrorCode 10 : Filename title doesn't match the track title tag
        printTrackErrorInfo(errorCode, t.fileNameList[5].rsplit('.', 1)[0], t.title)
    elif errorCode == 11: # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
        printTrackErrorInfo(errorCode, 'Here is the list of missing tags:', trackTester.missingTags)
    elif errorCode == 12: # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
        printTrackErrorInfo(errorCode, sorted(t.performers), sorted(t.composedPerformer))
    elif errorCode == 13: # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
        printTrackErrorInfo(errorCode, 'Here is the list of misordered tags:', trackTester.missorderedTag)
    elif errorCode == 14: # ErrorCode 14 : Computed album total track is not equal to the track total track tag
        printTrackErrorInfo(errorCode, t.totalTrack, trackTester.album.totalTrack)
    elif errorCode == 15: # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
        printTrackErrorInfo(errorCode, t.totalDisc, trackTester.album.totalDisc)
    elif errorCode == 16: # ErrorCode 16 : Computed album yeas is not equal to the track year tag
        printTrackErrorInfo(errorCode, t.year, trackTester.album.year)
    elif errorCode == 18: # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
        printTrackErrorInfo(errorCode, computeNamingConventionString(), 'AC-DC - 1978 - Powerage - 105 - AC-DC - Sin City')


def _printErroredAlbumsReport_aux(errorCode):
    if errorCode == 17: # ErrorCode 17 : Year is not the same on all physical files of the album
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
    # ErrorCode 09 : Title remix artist doesn't match the filename artist
    # ErrorCode 10 : Filename title doesn't match the track title tag
    elif errorCode == 3 or errorCode == 5 or errorCode == 7 or errorCode == 8 or errorCode == 10:
        location1 = 'From Filename          '
        location2 = 'From Track Tags        '
    # ErrorCode 04 : Foldername year doesn't math the track year tag
    # ErrorCode 06 : Foldername album doesn't match the track album
    elif errorCode == 4 or errorCode == 6:
        location1 = 'From Foldername        '
        location2 = 'From Track Tags        '
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    elif errorCode == 9:
        location1 = 'From Filename          '
        location2 = 'From Computed Remix    '
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 11:
        location1 = 'Missing Tags           '
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    elif errorCode == 12:
        location1 = 'From Performer Tag     '
        location2 = 'From Computed Performer'
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    elif errorCode == 13:
        location1 = 'Missordered Tags       '
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    # ErrorCode 16 : Computed album yeas is not equal to the track year tag
    elif errorCode == 14 or errorCode == 15 or errorCode == 16:
        location1 = 'From Track Tags        '
        location2 = 'From Computed Album    '
    elif errorCode == 17:
        location1 = 'Expected Pattern       '
        location2 = 'Example                '
    elif errorCode == 18:
        location1 = 'Expected Pattern       '
        location2 = 'Example                '
    print('| | | {:02d} {} -> {} : \'{}\''.format(errorCode, topic, location1, string1))
    print('| | |                            {} : \'{}\''.format(location2, string2))
