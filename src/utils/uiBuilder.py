# Python imports
import icu
# Project imports
from src.utils.tools import convertBytes


# Prints script credentials
def printCredentials(scriptVersion):
    print('##----------------------------------------##')
    print('##                                        ##')
    print('##   OstrichRemover.py - version {}    ##'.format(scriptVersion))
    print('##                                        ##')
    print('##----------------------------------------##\n')


# Displays an error message when the user didn't provided either scan of fill argument
def printMissingArguments():
    print('  You must provide the -s (--scan) or the -f (--fill) argument to the command, depending on your need\n')
    print('> Exiting OstrichRemover.py')


# Displays an error message when the user path is invalid
def printInvalidPath(path):
    print('  The path \'{}\' is invalid...'.format(path))
    print('  It must end with a / or an \\, depending on your system\n')
    print('> Exiting OstrichRemover.py')


# Displays an error message when the folder structure tested is not according to ManaZeak naming convention
def printInvalidFolderStructure(done, totalTrack, verb):
    print('\n  Unable to properly {} path ({} / {} tracks {}ed)'.format(verb, done, totalTrack, verb))
    print('>  The folder structure does not exactly match the ManaZeak naming convention')
    print('>  Ensure you don\'t have any release mis-named or exotic tree structures')


# Prints script 'man' page
def printHelp():
    print('  Script usage')
    print('> python OstrichRemover.py ./path/to/library    : Do a crawling on the given folder')
    print('> python OstrichRemover.py -h                   : Displays the script help menu')


# Prints the first message before scanning folder information
def printRetrieveFolderInfo():
    print('  Retrieving folder information...\n')


# Prints the studied folder and its information
def printRootFolderInfo(folderInfo):
    print('  Files and folders information')
    print('> Folder name  : {}'.format(folderInfo.folder))
    print('> File count   : {:5d}'.format(folderInfo.filesCounter))
    print('> Folder count : {:5d}'.format(folderInfo.foldersCounter))
    print('> Folder size  : {}\n'.format(convertBytes(folderInfo.folderSize)))
    print('  Library informations')
    print('> Artist(s) : {:6d}\n> Album(s)  : {:6d}'.format(folderInfo.artistsCounter, folderInfo.albumsCounter))
    print('> Track(s)  : {:6d}\n> Cover(s)  : {:6d}\n'.format(folderInfo.tracksCounter, folderInfo.coversCounter))
    print('  Audio files informations')
    print('> FLAC  : {:6d} file(s) ({} %)\n> MP3   : {:6d} file(s) ({} %)'.format(folderInfo.flacCounter, folderInfo.flacPercentage, folderInfo.mp3Counter, folderInfo.mp3Percentage))
    print('> Total : {:6d} file(s)\n'.format(folderInfo.flacCounter + folderInfo.mp3Counter))
    print('  Artworks informations')
    print('> PNG   : {:6d} file(s) ({} %)\n> JPG   : {:6d} file(s) ({} %)'.format(folderInfo.pngCounter, folderInfo.pngPercentage, folderInfo.jpgCounter, folderInfo.jpgPercentage))
    print('> Total : {:6d} file(s)\n'.format(folderInfo.pngCounter + folderInfo.jpgCounter))


# Prints a detailled view of a given track. Very verbose, use carefully with big libraries (unless you're ok with the shell dying in the field!)
def printDetailledTrack(track):
    print('Title : {}'.format(track.title))
    print('Artists : {}'.format(track.artists))
    print('Album : {}'.format(track.albumTitle))
    print('Year : {}'.format(track.year))
    print('Performers : {}'.format(track.performers))
    print('Composers : {}'.format(track.composers))
    print('Producer : {}'.format(track.producer))
    print('Track n° : {}'.format(track.trackNumber))
    print('Track total : {}'.format(track.totalTrack))
    print('Disc n° : {}'.format(track.discNumber))
    print('Disc total : {}'.format(track.totalDisc))
    print('Remixer : {}'.format(track.remix))
    print('Featuring : {}'.format(track.feat))
    print('FileType : {}'.format(track.fileType))
    print('Raw FileName : {}'.format(track.fileName))
    print('FileName list : {}'.format(track.fileNameList))
    print('FolderName list: {}'.format(track.folderNameList))
    print('Path list : {}\n'.format(track.pathList))


# Prints the scan begin message
def printScanStart(targetFolder, totalTracks, possibleErrors):
    print('  Folder scan : {} track(s) to test ({} errors tested per track)'.format(totalTracks, possibleErrors))
    print('> Scanning files in folder \'{}\' and all its sub-directories...\n'.format(targetFolder))


# Prints the scan progression
def printScanProgress(percentage, previousLetter, currentLetter, errorCounter, scannedTracks, purity):
    print('> {:02d}% -- from {} to {} -- {:6d} tracks (purity of {} %) with {} errors'.format(percentage, previousLetter,
                                                                                        currentLetter, scannedTracks, purity, errorCounter))


# Print the scand end message
def printScanEnd(duration, errorCounter, totalTracks, purity):
    print('  Folder analysis done! It took {} seconds to perform the scan'.format(duration))
    print('> {} errors on {} tracks (purity : {} %)'.format(errorCounter, totalTracks, purity))


# Prints the scan begin message
def printFillStart(targetFolder, totalTracks):
    print('  Folder scan : {} track(s) to fill'.format(totalTracks))
    print('> Tagging files in folder \'{}\' and all its sub-directories...\n'.format(targetFolder))


# Prints the scan progression
def printFillProgress(percentage, filledTracks):
    print('> {:02d}% -- {:6d} tracks had their tags filled'.format(percentage, filledTracks))


# Print the scand end message
def printFillEnd(duration, filledTracks):
    print('  Tag filling is done! It took {} seconds to perform the fill'.format(duration))
    print('> {} tracks had their tags filled'.format(filledTracks))


# Prints the scan begin message
def printAnalyzeStart(targetFolder, totalFiles):
    print('  Folder analysis : {} file(s) to analyze'.format(totalFiles))
    print('> Analysing JSON files in folder \'{}\'\n'.format(targetFolder))


# Print the meta analysis sum up
def printAnalyzeStatus(metaAnalyzer):
    ma = metaAnalyzer.metaAnalysis
    fd = metaAnalyzer.dumps[0]['folderInfo'] # First dump, usefull for totals
    ld = metaAnalyzer.dumps[len(metaAnalyzer.dumps) - 1]['folderInfo'] # Last dump, usefull for totals
    print('  Meta analysis sum up (from {} to {})\n'.format(ma['dateFrom'], ma['dateTo']))
    print('  Library\'s size increased by {} ({} -> {})'.format(convertBytes(ma['sizeDelta']), convertBytes(fd['size']), convertBytes(ld['size'])))
    print('> {} file(s) have been added ({} -> {} file(s))'.format(ma['filesDelta'], fd['files'], ld['files']))
    print('> {} folder(s) have been created ({} -> {} folder(s))\n'.format(ma['foldersDelta'], fd['folders'], ld['folders']))
    print('  Library\'s addition detail')
    print('> {} artist(s) were added ({} -> {} artist(s))'.format(ma['artistsDelta'], fd['artistsCount'], ld['artistsCount']))
    print('> {} album(s) were added ({} -> {} album(s))'.format(ma['albumsDelta'], fd['albumsCount'], ld['albumsCount']))
    print('> {} track(s) were added ({} -> {} track(s))'.format(ma['tracksDelta'], fd['tracksCount'], ld['tracksCount']))
    print('> {} cover(s) were added ({} -> {} cover(s))\n'.format(ma['coversDelta'], fd['coversCount'], ld['coversCount']))
    print('  Quality detail')
    print('> Purity grade increased by {}% ({}% -> {}%)'.format(ma['purityDelta'], fd['purity'], ld['purity']))
    print('> {} flac file(s) were added ({} -> {} flac(s))'.format(ma['flacDelta'], fd['flacCount'], ld['flacCount']))
    print('> {} mp3 file(s) were added ({} -> {} mp3(s))'.format(ma['mp3Delta'], fd['mp3Count'], ld['mp3Count']))
    print('> {} jpg file(s) were added ({} -> {} jpg(s))'.format(ma['jpgDelta'], fd['jpgCount'], ld['jpgCount']))
    print('> {} png file(s) were added ({} -> {} png(s))\n'.format(ma['pngDelta'], fd['pngCount'], ld['pngCount']))


# Print the scand end message
def printAnalyzeEnd(duration, analyzedFiles):
    print('  Folder analysis is done! It took {} seconds to perform the analysis'.format(duration))
    print('> {} json(s) have been analyzed'.format(analyzedFiles))


# Prints the scan begin message
def printCleanStart(targetFolder, totalTracks):
    print('  Folder scan : {} track(s) to clean'.format(totalTracks))
    print('> Removing tags in folder \'{}\' and all its sub-directories...\n'.format(targetFolder))


# Prints the scan progression
def printCleanProgress(percentage, cleanedTracks):
    print('> {:02d}% -- {:6d} tracks had their tags removed'.format(percentage, cleanedTracks))


# Print the scand end message
def printCleanEnd(duration, cleanedTracks):
    print('  Tag cleaning is done! It took {} seconds to perform the clean'.format(duration))
    print('> {} tracks had their tags cleaned'.format(cleanedTracks))


# Print a line break in console
def printLineBreak():
    print('')


# -v, --verbose : Crawl albumTesters array and print all errors as a tree
def printErroredTracksReport(albumTesters):
    print('\n  Errors in tree:')
    currentArtist = ''
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        # Current Artist has changed : update UI w/ new parsed artist
        if currentArtist != albumPathList[len(albumPathList) - 2]:
            print('+ {}'.format(albumPathList[len(albumPathList) - 2]))
            currentArtist = albumPathList[len(albumPathList) - 2]
        # Print current album name
        print('| + {}'.format(albumPathList[len(albumPathList) - 1]))
        if len(albumTester.errors) > 0:
            print('| | + Errors that are album wide:')
            print('| | |----------------------------')
            for error in albumTester.errors:
                _printErroredAlbumsReport_aux(error.value['errorCode'])
        trackErrorWarning = False
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                if trackErrorWarning is False:
                    trackErrorWarning = True
                    print('| | + Errors that are track wide:')
                    print('| | |----------------------------')
                print('| | + {}'.format(trackTester.track.fileName))
                for error in trackTester.errors:
                    _printErroredTracksReport_aux(error.value['errorCode'], trackTester)


# Auxilliary, print an error about a given track
def _printErroredTracksReport_aux(errorCode, trackTester):
    # For accented char sorting
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
    # ErrorCode 16 : Computed album year is not equal to the track year tag
    elif errorCode == 16:
        printTrackErrorInfo(errorCode, t.year, trackTester.album.year)
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    elif errorCode == 18:
        printTrackErrorInfo(errorCode, computeNamingConventionString(), 'AC-DC - 1978 - Powerage - 105 - AC-DC - Sin City')
    # ErrorCode 19 : Cover is not a 1000x1000 jpg image
    elif errorCode == 19:
        printTrackErrorInfo(errorCode, 'Cover dimensions are incorrect.', 'Embeded image should be 1000x1000.')
    # ErrorCode 20 : Track has no cover
    elif errorCode == 20:
        printTrackErrorInfo(errorCode, 'Cover is missing from file.', 'Please embed an image file in the track.')
    # ErrorCode 21 : Release artist folder name doesn't match the track album artist tag
    elif errorCode == 21:
        printTrackErrorInfo(errorCode, t.fileNameList[0], t.albumArtist)
    # ErrorCode 22 : Cover format is not optimized (not jpg)
    elif errorCode == 22:
        printTrackErrorInfo(errorCode, 'image/jpeg', t.coverType)
    # ErrorCode 23 : BPM is not an integer
    elif errorCode == 23:
        printTrackErrorInfo(errorCode, 'BPM must be an integer', t.bpm)
    # ErrorCode 24 : Release year is not realistic (< 1900 or > today)
    elif errorCode == 24:
        printTrackErrorInfo(errorCode, t.year, '[ 1900 ; Today.year ]')
    # ErrorCode 25 : Invalid country value. Use NATO country notation with 3 capital letters
    elif errorCode == 25:
        printTrackErrorInfo(errorCode, t.lang, 'XXX -> replaced with the country trigram describe by OTAN')
    # ErrorCode 26 : Unexisting country trigram. Check existing NATO values
    elif errorCode == 26:
        printTrackErrorInfo(errorCode, t.lang, 'Check existing values at https://en.wikipedia.org/wiki/List_of_NATO_country_codes')
    # ErrorCode 27 : Inconsistent genre tag
    elif errorCode == 27:
        printTrackErrorInfo(errorCode, t.genres, 'Invalid genre structure')
    # ErrorCode 28 : Unexisting genre tag
    elif errorCode == 28:
        printTrackErrorInfo(errorCode, t.genres, 'Invalid genre value')
    # ErrorCode 29 : Invalid compilation tag
    elif errorCode == 29:
        printTrackErrorInfo(errorCode, t.compilation, 'Invalid compilation value')
    # ErrorCode 32 : A tag in file doesn't have a unique field
    elif errorCode == 32:
        printTrackErrorInfo(errorCode, t.title, 'Each tag must have only one field for its data')
    # ErrorCode 35 : Cover has no description in tag
    elif errorCode == 35:
        printTrackErrorInfo(errorCode, t.coverDesc, 'Cover description is missing')
    # ErrorCode 36 : Cover description doesn't match the fileName
    elif errorCode == 36:
        printTrackErrorInfo(errorCode, t.coverDesc, 'Cover description doesn\'t match the convention')
    # ErrorCode 37 : Release date tag is not using YYYY-MM-DD format
    elif errorCode == 37:
        printTrackErrorInfo(errorCode, t.date, 'Release date is not a valid date')
    # ErrorCode 39 : Folder name release date doesn't match the track release date tag
    elif errorCode == 39:
        printTrackErrorInfo(errorCode, t.date, 'Release date doesn\'t match the album folder name release date')


# Auxilliary, print an error about a given album
def _printErroredAlbumsReport_aux(errorCode):
    # ErrorCode 17 : Year is not the same on all physical files of the album
    if errorCode == 17:
        printTrackErrorInfo(errorCode, 'All files in folder does not have the same year', 'Rename them properly to remove this error')
    # ErrorCode 30 : Label tag is not consistent over album tracks
    elif errorCode == 30:
        printTrackErrorInfo(errorCode, 'Inconsitent label across album', 'Please set each label tag on file with the same value')
    # ErrorCode 31 : Label tag is not consistent over album tracks
    elif errorCode == 31:
        printTrackErrorInfo(errorCode, 'Inconsitent language across album', 'Please set each language tag on file with the same value')
    # ErrorCode 33 : The year tag doesn't match the year in released date tag
    elif errorCode == 33:
        printTrackErrorInfo(errorCode, 'Inconsistent year', 'Release date year doesn\'t match the year tag')
    # ErrorCode 34 : There is no cover, or there are more than one cover
    elif errorCode == 34:
        printTrackErrorInfo(errorCode, 'Cover count error', 'No cover, or invalid amount of cover in album')
    # ErrorCode 38 : Release date is not consistent accross album
    elif errorCode == 38:
        printTrackErrorInfo(errorCode, 'Inconsistent release date accross album', 'Please set each release date tag on file with the same value')


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
    # ErrorCode 21 : Release artist folder name doesn't match the track album artist tag
    elif errorCode == 4 or errorCode == 6 or errorCode == 21:
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
    # ErrorCode 16 : Computed album year is not equal to the track year tag
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
    # ErrorCode 19 : Cover is not a 1000x1000 jpg image
    # ErrorCode 20 : Track has no cover
    # ErrorCode 34 : There is no cover, or there are more than one cover
    # ErrorCode 35 : Cover has no description in tag
    # ErrorCode 36 : Cover description doesn't match the fileName
    elif errorCode == 19 or errorCode == 20 or errorCode == 34 or errorCode == 35 or errorCode == 36:
        location1 = 'From Cover Tag         '
    # ErrorCode 22 : Cover format is not optimized (not jpg)
    elif errorCode == 22:
        location1 = 'Expected cover mimetype'
        location2 = 'Cover mimetype         '
    # ErrorCode 23 : BPM is not an integer
    elif errorCode == 23:
        location1 = 'Expected type          '
        location2 = 'From Track Tag         '
    # ErrorCode 24 : Release year is not realistic (< 1900 or > today)
    elif errorCode == 24:
        location1 = 'From Track Tag         '
        location2 = 'Expected bounds        '
    # ErrorCode 25 : Invalid country value. Use NATO country notation with 3 capital letters
    # ErrorCode 26 : Unexisting country trigram. Check existing NATO values
    elif errorCode == 25 or errorCode == 26:
        location1 = 'From Track Tag         '
        location2 = 'Expected value         '
    # ErrorCode 27 : Inconsistent genre tag
    # ErrorCode 28 : Unexisting genre tag
    # ErrorCode 29 : Invalid compilation tag
    elif errorCode == 27 or errorCode == 28 or errorCode == 29:
        location1 = 'From Track Tags        '
    # ErrorCode 30 : Label tag is not consistent over album tracks
    elif errorCode == 30:
        location1 = 'From label tag on files'
        location2 = 'Action                 '
    # ErrorCode 31 : Lang tag is not consistent over album tracks
    elif errorCode == 31:
        location1 = 'From lang tag on files '
        location2 = 'Action                 '
    # ErrorCode 32 : Lang tag is not consistent over album tracks
    elif errorCode == 32:
        location1 = 'From track             '
        location2 = 'Action                 '
    # ErrorCode 33 : The year tag doesn't match the year in released date tag
    elif errorCode == 33:
        location1 = 'From year              '
        location2 = 'From release year      '
    # ErrorCode 37 : Release date tag is not using YYYY-MM-DD format
    elif errorCode == 37:
        location1 = 'From release year      '
    # ErrorCode 38 : Release date is not consistent accross album
    # ErrorCode 39 : Folder name release date doesn't match the track release date tag
    elif errorCode == 38 or errorCode == 39:
        location1 = 'From date tag on files '
        location2 = 'Action                 '
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
    # ErrorCode 24 : Release year is not realistic (< 1900 or > today)
    elif errorCode == 1 or errorCode == 3 or errorCode == 4 or errorCode == 24:
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
    # ErrorCode 19 : Cover is not a 1000x1000 jpg image
    # ErrorCode 20 : Track has no cover
    # ErrorCode 34 : There is no cover, or there are more than one cover
    # ErrorCode 35 : Cover has no description in tag
    # ErrorCode 36 : Cover description doesn't match the fileName
    elif errorCode == 19 or errorCode == 20 or errorCode == 34 or errorCode == 35 or errorCode == 36:
        topic = '-------- Cover Error'
    # ErrorCode 21 : Release artist folder name doesn't match the track album artist tag
    elif errorCode == 21:
        topic = '------- Album Artist'
    # ErrorCode 22 : Cover format is not optimized (not jpg)
    elif errorCode == 22:
        topic = '------- Cover format'
    # ErrorCode 23 : BPM is not an integer
    elif errorCode == 23:
        topic = '---------------- BPM'
    # ErrorCode 25 : Invalid country value. Use NATO country notation with 3 capital letters
    # ErrorCode 26 : Unexisting country trigram. Check existing NATO values
    # ErrorCode 31 : Lang tag is not consistent over album tracks
    elif errorCode == 25 or errorCode == 26 or errorCode == 31:
        topic = '----------- Language'
    # ErrorCode 27 : Inconsistent genre tag
    # ErrorCode 28 : Unexisting genre tag
    elif errorCode == 27 or errorCode == 28:
        topic = '-------------- Genre'
    # ErrorCode 29 : Invalid compilation tag
    elif errorCode == 29:
        topic = '-------- Compilation'
    # ErrorCode 30 : Label tag is not consistent over album tracks
    elif errorCode == 30:
        topic = '-------- Album label'
    # ErrorCode 32 : A tag in file doesn't have a unique field
    elif errorCode == 32:
        topic = '---------- Tag error'
    # ErrorCode 33 : The year tag doesn't match the year in released date tag
    # ErrorCode 38 : Release date is not consistent accross album
    # ErrorCode 39 : Folder name release date doesn't match the track release date tag
    elif errorCode == 33 or errorCode == 37 or errorCode == 38 or errorCode == 39:
        topic = '------- Release date'
    return topic


# Display the naming convention (see https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention)
def computeNamingConventionString():
    return '%releaseArtist% - %year% - %album% - %disc n°%%track n°% - %artist% - %title%'
